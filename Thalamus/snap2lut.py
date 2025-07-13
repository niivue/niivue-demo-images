import sys
import json

def parse_snap_lut(filepath):
    index = []
    labels = []
    R = []
    G = []
    B = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            try:
                idx = int(parts[0])
                label = ' '.join(parts[1:-4])
                r, g, b, a = map(int, parts[-4:])
            except ValueError:
                continue
            index.append(idx)
            labels.append(label)
            R.append(r)
            G.append(g)
            B.append(b)

    return {
        "R": R,
        "G": G,
        "B": B,
        "I": index,
        "labels": labels

    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python snap2niivue_lut.py Thalamic_Nuclei-ColorLUT.txt")
        sys.exit(1)

    lut = parse_snap_lut(sys.argv[1])
    json_file = sys.argv[1].replace('.txt', '.json')
    with open(json_file, 'w') as f:
        json.dump(lut, f, indent=2)
    print(f"Saved NiiVue label colormap JSON: {json_file}")
