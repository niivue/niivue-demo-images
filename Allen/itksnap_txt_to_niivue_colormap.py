import json

def parse_label_file(txt_path, output_path):
    cmap = {
        "R": [0],
        "G": [0],
        "B": [0],
        "I": [0],
        "labels": ["Air"],
    }

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 8:
                continue  # skip malformed lines
            try:
                index = int(parts[0])
                r = int(parts[1])
                g = int(parts[2])
                b = int(parts[3])
                label_str = line.strip().split('"')[-2]  # get quoted part
                label = label_str.split(' ')[0]  # extract prefix before space
            except Exception as e:
                print(f"Skipping line due to parse error: {line}")
                continue

            cmap["I"].append(index)
            cmap["R"].append(r)
            cmap["G"].append(g)
            cmap["B"].append(b)
            cmap["labels"].append(label)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cmap, f, indent=2)

    print(f"Saved colormap JSON to: {output_path}")

if __name__ == "__main__":
    parse_label_file("itksnap_label_description_Br.txt", "AllenAtlas.json")
