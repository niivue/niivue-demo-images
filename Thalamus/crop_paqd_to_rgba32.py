import nibabel as nib
import numpy as np
import sys
from pathlib import Path

def crop_and_convert(input_path):
    input_path = Path(input_path)
    base = input_path.name.replace('.nii.gz', '').replace('.nii', '')
    output_path = input_path.parent / f"{base}_cropped.nii"

    img = nib.load(str(input_path))
    data = img.get_fdata()
    affine = img.affine

    while data.ndim < 5:
        data = data[..., np.newaxis]

    if data.shape[4] != 4:
        raise ValueError("Expected RGBA image with 4 channels in 5th dimension.")

    # Binary mask for non-zero RGBA values
    mask = np.any(data != 0, axis=(3, 4))
    coords = np.array(np.nonzero(mask))
    xmin, ymin, zmin = coords.min(axis=1)
    xmax, ymax, zmax = coords.max(axis=1) + 1

    # Add 1-voxel zero padding, clipped to bounds
    pad = 1
    xmin_p = max(xmin - pad, 0)
    xmax_p = min(xmax + pad, data.shape[0])
    ymin_p = max(ymin - pad, 0)
    ymax_p = min(ymax + pad, data.shape[1])
    zmin_p = max(zmin - pad, 0)
    zmax_p = min(zmax + pad, data.shape[2])

    cropped = data[xmin_p:xmax_p, ymin_p:ymax_p, zmin_p:zmax_p, 0, :]
    rgba_flat = np.ascontiguousarray(cropped.astype(np.uint8)).reshape(-1, 4)
    rgba32 = rgba_flat.view(np.uint32).reshape(cropped.shape[:3])
    # Compute new affine by translating origin voxel in world space
    # origin_voxel = np.array([(xmin-1), (ymin-1), (zmin-1), 1])
    origin_voxel = np.array([xmin_p, ymin_p, zmin_p, 1])
    new_origin_world = affine @ origin_voxel
    new_affine = affine.copy()
    new_affine[:3, 3] = new_origin_world[:3]
    # Save as UINT32 then patch to DT_RGBA32
    img_out = nib.Nifti1Image(rgba32, new_affine)
    img_out.set_data_dtype(np.uint32)
    nib.save(img_out, str(output_path))

    # Patch datatype in header to DT_RGBA32 (2304)
    with open(output_path, 'r+b') as f:
        # Set intent_code (2 bytes at offset 68)
        f.seek(68)
        f.write((1002).to_bytes(2, byteorder='little'))  # NIFTI_INTENT_LABEL
        # Set datatype (2 bytes at offset 70)
        f.seek(70)
        f.write((2304).to_bytes(2, byteorder='little'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python crop_paqd_to_rgba32.py <input_file.nii[.gz]>")
        sys.exit(1)
    crop_and_convert(sys.argv[1])
