import nibabel as nib
import numpy as np
from skimage.measure import marching_cubes
import gzip
import struct
import json
import os
import sys
from scipy.ndimage import gaussian_filter

try:
    import pymeshlab
    HAS_PYMESHLAB = True
except ImportError:
    HAS_PYMESHLAB = False
    print("Warning: pymeshlab not installed, mesh simplification will be skipped.")

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

def simplify_mesh(verts, faces, reduction_fraction):
    if not HAS_PYMESHLAB or reduction_fraction >= 1.0:
        return verts, faces
    try:
        ms = pymeshlab.MeshSet()
        m = pymeshlab.Mesh(vertex_matrix=verts, face_matrix=faces)
        ms.add_mesh(m, "mesh")
        target = int(faces.shape[0] * reduction_fraction)
        ms.apply_filter("meshing_decimation_quadric_edge_collapse", targetfacenum=target)
        simplified = ms.current_mesh()
        return simplified.vertex_matrix(), simplified.face_matrix()
    except Exception as e:
        print(f"  Simplification failed: {e}. Skipping reduction.")
        return verts, faces

def extract_label_meshes(nifti_path, blur_fwhm=0.0, reduction_fraction=1.0):
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"File not found: {nifti_path}")

    print(f"Loading {nifti_path}")
    nii = nib.load(nifti_path)
    data = nii.get_fdata()
    affine = nii.affine.astype(np.float64)

    if data.ndim == 3:
        data = data[..., np.newaxis]  # promote to 4D

    X, Y, Z, N = data.shape
    basename = os.path.splitext(os.path.basename(nifti_path))[0]
    if basename.endswith(".nii"):
        basename = os.path.splitext(basename)[0]

    for i in range(N):
        vol = data[:, :, :, i].astype(np.float32)
        if np.max(vol) <= 0:
            print(f"Skipping region {i+1}: all-zero volume")
            continue

        if blur_fwhm > 0:
            sig = blur_fwhm / np.sqrt(8 * np.log(2))  # FWHM to sigma
            vol = gaussian_filter(vol, sigma=sig)

        isosurface = 0.5 * np.max(vol)

        try:
            verts, faces, _, _ = marching_cubes(vol, level=isosurface)
            faces = faces[:, ::-1]  # Ensure counter-clockwise winding
        except Exception as e:
            print(f"Skipping region {i+1} due to error: {e}")
            continue

        verts = verts.astype(np.float64)
        verts_hom = np.hstack([verts, np.ones((verts.shape[0], 1))])
        verts_world = np.dot(verts_hom, affine.T)[:, :3]

        verts_world, faces = simplify_mesh(verts_world, faces, reduction_fraction)
        output_name = f"{basename}_{i+1}.mz3"
        print(f"Writing {output_name} with {len(verts_world)} vertices and {len(faces)} faces")
        write_mz3(output_name, faces, verts_world)



if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python atlas2mesh.py input.nii[.gz] [blur_fwhm] [reduction_fraction]")
        print("       blur_fwhm in voxels (default: 0.0)")
        print("       reduction_fraction (0.0 - 1.0, default: 1.0 for no simplification)")
        sys.exit(1)

    nifti_path = sys.argv[1]
    blur_fwhm = float(sys.argv[2]) if len(sys.argv) >= 3 else 0.0
    reduction_fraction = float(sys.argv[3]) if len(sys.argv) == 4 else 1.0

    extract_label_meshes(nifti_path, blur_fwhm=blur_fwhm, reduction_fraction=reduction_fraction)