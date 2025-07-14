import csv
import random
import json

input_csv = 'linked_output.csv'
output_json = 'colormap.json'

# Load and parse semicolon-delimited CSV
entries = []
with open(input_csv, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        if not row or row[0].startswith('#'):
            continue
        try:
            index = int(row[0])
            label = row[2].strip()
            entries.append((index, label))
        except (IndexError, ValueError):
            continue  # skip malformed rows

# Sort by label index
entries.sort(key=lambda x: x[0])

# Build colormap dictionary
cmap = {
    "R": [0],
    "G": [0],
    "B": [0],
    "I": [0],
    "labels": ["air"]
}

for idx, label in entries:
    cmap["R"].append(random.randint(0, 255))
    cmap["G"].append(random.randint(0, 255))
    cmap["B"].append(random.randint(0, 255))
    cmap["I"].append(idx)
    cmap["labels"].append(label)

# Save to JSON file
with open(output_json, 'w') as f:
    json.dump(cmap, f, indent=2)

print(f"Saved colormap to: {output_json}")
