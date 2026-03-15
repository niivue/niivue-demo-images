#!/usr/bin/env python3
"""
subsamp2.py

Simple downsample-by-2 (factor 2) with trilinear interpolation.
Usage:
    python subsamp2.py input.nii.gz output.nii.gz

Dependencies:
    pip install nibabel numpy scipy
"""
import sys
import numpy as np
import nibabel as nib
from scipy.ndimage import map_coordinates
from math import ceil

def subsamp2_trilinear(in_img):
    data = in_img.get_fdata(dtype=np.float32)  # float for interpolation
    affine = in_img.affine.copy()
    hdr = in_img.header.copy()

    # Only handle 3D/4D images; if 4D, resample each volume independently
    if data.ndim == 4:
        vols = data.shape[3]
        spatial_shape = data.shape[:3]
    elif data.ndim == 3:
        vols = 1
        spatial_shape = data.shape
        data = data[..., np.newaxis]
    else:
        raise ValueError("Unsupported image dimensionality: {}".format(data.ndim))

    # new spatial shape: ceil(old / 2) to preserve physical extent as closely as possible
    new_shape = tuple(int(ceil(s / 2.0)) for s in spatial_shape)

    # Build new affine so that world coordinates cover the same physical extent:
    # new_affine = old_affine @ diag([2,2,2,1])
    scale_mat = np.diag([2.0, 2.0, 2.0, 1.0])
    new_affine = affine @ scale_mat

    # Precompute inverse of original affine to map world -> old voxel coords
    inv_affine = np.linalg.inv(affine)

    # Generate grid of output voxel centers (i, j, k) in new image space
    # We'll compute corresponding coords in old voxel space for interpolation
    # Use indexing='ij' to match nibabel's i,j,k ordering
    zs, ys, xs = np.meshgrid(
        np.arange(new_shape[2]),
        np.arange(new_shape[1]),
        np.arange(new_shape[0]),
        indexing='xy'
    )
    # NOTE: meshgrid above returns (Y,X,Z) if using 'xy'; easier to build coords systematically:
    # Let's generate coordinates in (i, j, k) order
    i_coords, j_coords, k_coords = np.indices(new_shape, dtype=np.float64)
    # Flatten
    i_flat = i_coords.ravel()
    j_flat = j_coords.ravel()
    k_flat = k_coords.ravel()
    n_pts = i_flat.size

    # Convert new-voxel indices -> world coords using new_affine:
    ones = np.ones((n_pts,), dtype=np.float64)
    vox_new_h = np.vstack((i_flat, j_flat, k_flat, ones))  # shape (4, npts)
    world_coords = new_affine @ vox_new_h  # shape (4, npts)

    # Map world coords to old voxel coordinates:
    old_vox_coords_h = inv_affine @ world_coords
    old_x = old_vox_coords_h[0, :]
    old_y = old_vox_coords_h[1, :]
    old_z = old_vox_coords_h[2, :]

    # Prepare output array
    out_data = np.zeros((new_shape[0], new_shape[1], new_shape[2], vols), dtype=np.float32)

    # For each volume, perform trilinear interpolation (map_coordinates with order=1)
    # map_coordinates expects coords in order (dim, npoints) where dim indexes the array axes
    coords = np.vstack((old_x, old_y, old_z))
    for v in range(vols):
        vol = data[..., v]
        # mode='nearest' avoids NaNs at borders; you can change to 'constant' with cval=0 if preferred
        sampled = map_coordinates(vol, coords, order=1, mode='nearest')
        out_data[..., v] = sampled.reshape(new_shape)

    # Squeeze if original was 3D
    if out_data.shape[-1] == 1:
        out_data = out_data[..., 0]

    # Update header pixdim (voxel sizes) - header['pixdim'][1:4] are x,y,z voxel sizes
    old_pixdim = np.array(hdr.get_zooms()[:3], dtype=float)
    new_pixdim = tuple(old_pixdim * 2.0)
    hdr.set_zooms(new_pixdim + hdr.get_zooms()[3:])  # preserve time dim if present

    # Set new sform/qform to new_affine
    # nibabel wants the affine on the image object; pass new_affine into save call and set header q/s forms
    out_img = nib.Nifti1Image(out_data, new_affine, header=hdr)
    out_img.set_sform(new_affine)
    out_img.set_qform(new_affine)

    return out_img

def main():
    if len(sys.argv) != 3:
        print("Usage: python subsamp2.py input.nii.gz output.nii.gz")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    # Load input
    img = nib.load(in_path)
    out_img = subsamp2_trilinear(img)

    # Save output
    nib.save(out_img, out_path)
    print(f"Saved downsampled image to: {out_path}")
    print("New shape:", out_img.shape)
    print("New zooms (pixdim):", out_img.header.get_zooms())

if __name__ == "__main__":
    main()