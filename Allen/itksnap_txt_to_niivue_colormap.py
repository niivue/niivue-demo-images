import json

def parse_label_file(txt_path, output_path):
    entries = []

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 8:
                continue
            try:
                index = int(parts[0])
                r = int(parts[1])
                g = int(parts[2])
                b = int(parts[3])
                label_str = line.strip().split('"')[-2]
                label = label_str.split(' ')[0]
                entries.append((index, r, g, b, label))
            except Exception as e:
                print(f"Skipping line due to parse error: {line}")

    # Sort by index
    entries.sort(key=lambda x: x[0])

    cmap = {
        "R": [0],
        "G": [0],
        "B": [0],
        # "I": [0],
        "labels": ["Air"],
    }

    for index, r, g, b, label in entries:
        cmap["R"].append(r)
        cmap["G"].append(g)
        cmap["B"].append(b)
        # cmap["I"].append(index)
        cmap["labels"].append(label)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cmap, f, indent=2)

    print(f"Saved colormap JSON to: {output_path}")

if __name__ == "__main__":
    parse_label_file("itksnap_label_description_Br.txt", "AllenAtlas.json")
