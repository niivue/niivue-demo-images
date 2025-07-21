import sys
import os
import numpy as np
import nibabel as nib
import csv

def load_region_map(csv_path):
    region_names = []
    region_to_index = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            if len(row) > 1:
                try:
                    label_index = int(row[0])
                    region_name = row[1]
                    region_names.append(region_name)
                    region_to_index[region_name] = label_index
                except ValueError:
                    continue  # skip malformed lines
    return region_names, region_to_index


def main():
    if len(sys.argv) < 3:
        print("Usage: python julich2paqd.py atlas.csv folder/ [lh|rh]")
        sys.exit(1)

    csv_path = sys.argv[1]
    root_dir = sys.argv[2]
    hemi = sys.argv[3] if len(sys.argv) > 3 else 'lh'

    region_names, region_to_index = load_region_map(csv_path)
    volumes = []
    labels = []

    print(f"Searching for {len(region_names)} regions in '{root_dir}' for hemisphere '{hemi}'")

    for idx, name in enumerate(region_names):
        img_path = os.path.join(root_dir, name, f"{name}_{hemi}_MNI152.nii.gz")
        if os.path.exists(img_path):
            nii = nib.load(img_path)
            data = nii.get_fdata()
            if len(volumes) == 0:
                shape = data.shape
                affine = nii.affine
            else:
                assert data.shape == shape, f"Shape mismatch in {img_path}"
            volumes.append(data)
            labels.append(name)
        else:
            print(f"Skipping missing: {img_path}")

    if len(volumes) == 0:
        print("No region images found. Aborting.")
        sys.exit(1)

    data = np.stack(volumes, axis=-1)  # shape: (X, Y, Z, N)
    X, Y, Z, N = data.shape
    flat = data.reshape(-1, N)

    # Top-2
    top2_idx = np.argsort(flat, axis=1)[:, -2:]
    top2_prob = np.take_along_axis(flat, top2_idx, axis=1)

    # Ensure max prob is first
    swap = top2_prob[:, 1] > top2_prob[:, 0]
    top2_idx[swap] = top2_idx[swap][:, ::-1]
    top2_prob[swap] = top2_prob[swap][:, ::-1]

    # Convert probs to uint8 0–255
    top2_prob = np.clip(np.round(top2_prob * 255), 0, 255).astype(np.uint8)

    # Convert top2 indices to mapped label indices
    label_indices = np.array([region_to_index.get(name, 0) for name in labels], dtype=np.uint16)
    top2_idx = label_indices[top2_idx]
    top2_idx[top2_prob == 0] = 0

    # Stack RGBA
    rgba = np.stack([
        top2_idx[:, 0],
        top2_idx[:, 1],
        top2_prob[:, 0],
        top2_prob[:, 1]
    ], axis=1).astype(np.uint8)

    rgba = rgba.reshape(X, Y, Z, 1, 4)

    # Create NIfTI
    img = nib.Nifti1Image(rgba, affine)
    hdr = img.header
    hdr.set_data_dtype(np.uint8)
    hdr.set_xyzt_units('mm')
    hdr.set_intent(2004)
    hdr['intent_name'] = b'PAQD'
    hdr['dim'][0] = 5
    hdr['dim'][4] = 1
    hdr['dim'][5] = 4

    out_path = f"{os.path.basename(root_dir.rstrip('/'))}_{hemi}_paqd.nii.gz"
    nib.save(img, out_path)
    print(f"Saved PAQD image: {out_path}")

if __name__ == "__main__":
    main()
