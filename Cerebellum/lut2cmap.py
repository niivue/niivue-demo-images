import json

# Input and output filenames
input_file = "atl-Anatom.lut"
output_file = "atl-Anatom.json"

# Initialize colormap arrays with 'Air' as index 0
colormap = {
    "R": [0],
    "G": [0],
    "B": [0],
    "labels": ["Air"]
}

with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip empty or commented lines

        parts = line.split()
        if len(parts) < 5:
            continue  # skip malformed lines

        # Extract index, RGB, and label
        index = int(parts[0])  # ignored, assumed to be in order
        r = round(float(parts[1]) * 255)
        g = round(float(parts[2]) * 255)
        b = round(float(parts[3]) * 255)
        label = " ".join(parts[4:])

        colormap["R"].append(r)
        colormap["G"].append(g)
        colormap["B"].append(b)
        colormap["labels"].append(label)

# Write to JSON
with open(output_file, 'w') as f:
    json.dump(colormap, f, indent=2)

print(f"Saved colormap with {len(colormap['labels'])} labels to {output_file}")
