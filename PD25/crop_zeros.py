import nibabel as nib
import numpy as np
import sys
from pathlib import Path

def crop_mask_pad(input_path):
    input_path = Path(input_path)
    base = input_path.name.replace('.nii.gz', '').replace('.nii', '')
    output_path = input_path.parent / f"{base}_masked.nii.gz"

    img = nib.load(str(input_path))
    data = img.get_fdata(dtype=np.float32)  # use float32 to handle all types
    affine = img.affine
    dtype = img.get_data_dtype()
    orig_shape = data.shape

    # Ensure data is 3D or 4D
    if data.ndim == 3:
        data = data[..., np.newaxis]

    X, Y, Z, T = data.shape
    mask = np.any(data != 0, axis=3)
    if not np.any(mask):
        print("Image is fully zero; skipping.")
        return

    coords = np.array(np.nonzero(mask))
    xmin, ymin, zmin = coords.min(axis=1)
    xmax, ymax, zmax = coords.max(axis=1) + 1

    # Add 1-voxel padding but do not extend beyond original size
    pad = 1
    xmin_p = max(xmin - pad, 0)
    xmax_p = min(xmax + pad, X)
    ymin_p = max(ymin - pad, 0)
    ymax_p = min(ymax + pad, Y)
    zmin_p = max(zmin - pad, 0)
    zmax_p = min(zmax + pad, Z)

    cropped = data[xmin_p:xmax_p, ymin_p:ymax_p, zmin_p:zmax_p, :]

    # Preserve affine by shifting origin
    offset_voxel = np.array([xmin_p, ymin_p, zmin_p, 1])
    new_affine = affine.copy()
    new_affine[:3, 3] = (affine @ offset_voxel)[:3]

    # Restore original shape (3D if T==1)
    if orig_shape == cropped.shape[:-1]:
        cropped = np.squeeze(cropped, axis=3)

    # Report shapes
    print(f"Input shape:  {orig_shape}")
    print(f"Output shape: {cropped.shape}")
    
    img_out = nib.Nifti1Image(cropped.astype(dtype), new_affine)
    img_out.set_data_dtype(dtype)
    nib.save(img_out, str(output_path))
    print(f"Saved masked output to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mask_crop_pad_preserve.py <input_file.nii[.gz]>")
        sys.exit(1)
    crop_mask_pad(sys.argv[1])
