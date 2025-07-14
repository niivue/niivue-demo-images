import numpy as np
import nibabel as nib
import re

import numpy as np
import re

def load_mapping(txt_path):
    mapping = {}
    with open(txt_path, 'r') as f:
        for line in f:
            match = re.search(r'"[^"]*?(\d+)"', line)
            if match:
                raw_value_int = int(match.group(1))
                # Downcast to float32, then back to int to match voxel representation
                raw_value = int(np.float32(raw_value_int))
                label_id = int(line.split()[0])
                mapping[raw_value] = label_id
            else:
                print(f"Warning: could not parse line: {line.strip()}")

    keys = list(mapping.keys())
    if keys:
        print(f"Mapping loaded: {len(mapping)} entries")
        print(f"  Min raw value: {min(keys)}")
        print(f"  Max raw value: {max(keys)}")
    return mapping



def main():
    nii_path = 'annotation_full.nii.gz'
    txt_path = 'itksnap_label_description_Br.txt'
    output_path = 'annotation_remapped.nii.gz'

    nii = nib.load(nii_path)
    data_f = nii.get_fdata()
    print(f"Input image data type: {nii.get_data_dtype()}")
    print(f"Max value: {np.max(data_f):.2f}")
    print(f"Min value: {np.min(data_f):.2f}")
    print(f"Unique nonzero count: {np.count_nonzero(data_f)}")

    mapping = load_mapping(txt_path)
    mapped_data = np.zeros(data_f.shape, dtype=np.uint8)

    unique_vals = np.unique(data_f)
    hits, misses = 0, 0

    for val in unique_vals:
        if val == 0:
            continue
        closest = min(mapping.keys(), key=lambda k: abs(k - val))
        if abs(closest - val) > 0.5:
            print(f"Warning: No close match for value {val:.2f}")
            misses += 1
            continue
        mapped_data[data_f == val] = mapping[closest]
        hits += 1

    print(f"Mapped {hits} unique values. Missed {misses}.")

    new_img = nib.Nifti1Image(mapped_data, nii.affine, nii.header)
    new_img.set_data_dtype(np.uint8)
    nib.save(new_img, output_path)
    print(f"Saved remapped image as: {output_path}")

if __name__ == '__main__':
    main()
