import sys
import os
import numpy as np
import nibabel as nib

if len(sys.argv) != 2 or not sys.argv[1].endswith(('.nii', '.nii.gz')):
    print("Usage: python spam2paqd.py input_filename.nii[.gz]")
    sys.exit(1)

input_path = sys.argv[1]

# Create output filename by inserting "_paqd" before extension
if input_path.endswith('.nii.gz'):
    base = input_path[:-7]
    output_path = base + '_paqdnii.gz'
elif input_path.endswith('.nii'):
    base = input_path[:-4]
    output_path = base + '_paqd.nii.gz'
else:
    print("Input file must end with .nii or .nii.gz")
    sys.exit(1)

if not os.path.exists(input_path):
    print(f"Error: could not find input file: {input_path}")
    sys.exit(1)

# Load the input 4D probabilistic atlas (X, Y, Z, N)
nii = nib.load(input_path)
data = nii.get_fdata()
affine = nii.affine

X, Y, Z, N = data.shape
flat_data = data.reshape(-1, N)

# Get top two labels per voxel
top2_idx = np.argsort(flat_data, axis=1)[:, -2:]
top2_prob = np.take_along_axis(flat_data, top2_idx, axis=1)

# Ensure max prob is first
swap = top2_prob[:, 1] > top2_prob[:, 0]
top2_idx[swap] = top2_idx[swap][:, ::-1]
top2_prob[swap] = top2_prob[swap][:, ::-1]

# Convert to 0–255 uint8
top2_prob = np.clip(np.round(top2_prob * 255), 0, 255).astype(np.uint8)

# Increment labels (1-based); zero out where prob is 0
top2_idx = top2_idx + 1
top2_idx[top2_prob == 0] = 0

# Stack RGBA
rgba = np.stack([
    top2_idx[:, 0],
    top2_idx[:, 1],
    top2_prob[:, 0],
    top2_prob[:, 1],
], axis=1).astype(np.uint8)

# Reshape to 5D (X, Y, Z, 1, 4)
rgba = rgba.reshape(X, Y, Z, 1, 4)

# Save NIfTI with RGBA intent
img = nib.Nifti1Image(rgba, affine)
hdr = img.header
hdr.set_data_dtype(np.uint8)
hdr.set_xyzt_units('mm')
hdr.set_intent(2004)  # NIFTI_INTENT_RGBA_VECTOR
hdr['intent_name'] = b'PAQD'
hdr['dim'][0] = 5
hdr['dim'][4] = 1
hdr['dim'][5] = 4

nib.save(img, output_path)
print(f"PAQD image saved as {output_path}")
