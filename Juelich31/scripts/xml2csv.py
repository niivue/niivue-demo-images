import csv
import xml.etree.ElementTree as ET

# Input paths
xml_file = './maximum-probability-maps_MPMs_207-areas/JulichBrainAtlas_3.1_207areas_MPM_lh_MNI152.xml'
csv_file = 'JulichBrainAtlas_3.1_overview_areas.csv'
output_file = 'linked_output.csv'

# Parse XML: build map from ID to (grayvalue, name)
tree = ET.parse(xml_file)
root = tree.getroot()

id_to_gray_name = {}
for struct in root.findall(".//Structure"):
    id_str = struct.get("id")
    grayvalue = struct.get("grayvalue")
    name = struct.text.strip()
    id_to_gray_name[int(id_str)] = (int(grayvalue), name)

# Parse CSV and link
linked_rows = []
with open(csv_file, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        try:
            id_val = int(row[0])
            label = row[1]
            if id_val in id_to_gray_name:
                gray, name = id_to_gray_name[id_val]
                linked_rows.append([gray, label, name])
        except ValueError:
            continue  # skip header or invalid rows

# Write output
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    for row in linked_rows:
        writer.writerow(row)

print(f"Saved linked data to: {output_file}")
