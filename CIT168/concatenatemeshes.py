import os
import sys
import glob
import re
import gzip
import io
import struct
import json
import numpy as np

def read_mz3(filename):
    with open(filename, 'rb') as f:
        magic = f.read(2)
    if magic == b'\x1f\x8b':
        with gzip.open(filename, 'rb') as gz:
            raw = gz.read()
        f = io.BytesIO(raw)
    else:
        f = open(filename, 'rb')

    with f:
        hdr = f.read(16)
        magic, attr, nface, nvert, nskip = struct.unpack('<HHIII', hdr)
        if magic != 23117:
            raise ValueError(f"{filename} is not a valid MZ3 file.")
        f.read(nskip)
        faces = np.frombuffer(f.read(nface * 12), dtype=np.int32).reshape((-1, 3)) if attr & 1 else []
        verts = np.frombuffer(f.read(nvert * 12), dtype=np.float32).reshape((-1, 3)) if attr & 2 else []
        return faces, verts

def write_mz3(filename, faces, verts, scalars=None, json_data=None):
    ATTR_FACE   = 1
    ATTR_VERT   = 2
    ATTR_SCALAR = 8
    ATTR_JSON   = 64

    attr = 0
    if faces is not None:
        attr |= ATTR_FACE
    if verts is not None:
        attr |= ATTR_VERT
    if scalars is not None:
        attr |= ATTR_SCALAR
    json_bytes = b''
    if json_data is not None:
        attr |= ATTR_JSON
        json_bytes = json.dumps(json_data, separators=(',', ':')).encode('utf-8')
    nskip = len(json_bytes)

    nface = len(faces) if faces is not None else 0
    nvert = len(verts) if verts is not None else 0

    with gzip.open(filename, 'wb') as f:
        f.write(struct.pack('<HHIII', 0x5A4D, attr, nface, nvert, nskip))
        if nskip > 0:
            f.write(json_bytes)
        if faces is not None:
            f.write(faces.astype(np.int32).tobytes())
        if verts is not None:
            f.write(verts.astype(np.float32).tobytes())
        if scalars is not None:
            f.write(scalars.astype(np.float32).tobytes())

def combine_mz3s(base, output_name=None):
    json_file = (output_name or base) + '.json'
    if not os.path.exists(json_file):
        sys.exit(f"Error: JSON metadata file '{json_file}' not found.")

    json_data = json.load(open(json_file))
    mesh_files = sorted(glob.glob(f"{base}_*.mz3"))
    mesh_files = [f for f in mesh_files if re.match(rf"^{re.escape(base)}_\d+\.mz3$", os.path.basename(f))]
    if not mesh_files:
        sys.exit("No *_n.mz3 files found.")

    all_faces = []
    all_verts = []
    all_scalar = []
    vert_offset = 0

    for f in mesh_files:
        match = re.match(rf"^{re.escape(base)}_(\d+)\.mz3$", os.path.basename(f))
        label = int(match.group(1))
        faces, verts = read_mz3(f)
        nvert = verts.shape[0]
        all_faces.append(faces + vert_offset)
        all_verts.append(verts)
        all_scalar.append(np.full(nvert, label, dtype=np.float32))
        vert_offset += nvert

    out_file = (output_name or base) + '.mz3'
    write_mz3(out_file,
              np.vstack(all_faces),
              np.vstack(all_verts),
              np.concatenate(all_scalar),
              json_data)
    print(f"Combined mesh saved as: {out_file}")

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        print("Usage: python concatenatemeshes.py <mesh_prefix> [output_name]")
        sys.exit(1)
    combine_mz3s(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
