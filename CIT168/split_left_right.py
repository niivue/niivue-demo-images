import nibabel as nib
import numpy as np
import sys
from pathlib import Path

def split_volumes_left_right(input_path):
    input_path = Path(input_path)
    base = input_path.stem.replace(".nii", "")
    output_path = input_path.parent / f"{base}_split.nii.gz"

    nii = nib.load(str(input_path))
    data = nii.get_fdata()
    affine = nii.affine
    dtype = nii.get_data_dtype()

    if data.ndim != 4:
        raise ValueError("Input image must be 4D")

    X, Y, Z, T = data.shape
    mid = X // 2

    new_data = np.zeros((X, Y, Z, T * 2), dtype=np.float32)

    for t in range(T):
        vol = data[..., t]
        left_masked = np.zeros_like(vol)
        right_masked = np.zeros_like(vol)

        left_masked[:mid, :, :] = vol[:mid, :, :]
        right_masked[mid:, :, :] = vol[mid:, :, :]

        new_data[..., t * 2] = left_masked
        new_data[..., t * 2 + 1] = right_masked

    new_img = nib.Nifti1Image(new_data.astype(dtype), affine)
    new_img.set_data_dtype(dtype)
    nib.save(new_img, str(output_path))
    print(f"Saved split image to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_left_right.py input.nii.gz")
        sys.exit(1)
    split_volumes_left_right(sys.argv[1])
