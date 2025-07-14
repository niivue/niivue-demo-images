## About

The Allen Human Reference Atlas segments every voxel of the brain into 141 structures. The files here have been optimized for use with NiiVue, while retaining the same CC BY 4.0. Specifically, a NiiVue [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images) is provided. This atlas is aligned to the [ICBM 2009b Nonlinear Symmetric template](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009). The atlas has been losslessly cropped and uses a more compact data type. While converted images are provided, the processing scripts are also provided which may aid similar conversions.

## Creating new Atlases

The original annotation image (annotation_full.nii.gz) uses a float32 datatype to store integer-valued labels. While there are only 142 unique structures (including background), the label values span a wide range — from 10307 to 266441657. Unfortunately, values this large exceed the exact integer representation of float32 (see flintmax), leading to rounding errors. As a result, direct mapping from text files (which list true integer labels) to image voxel values fails unless this loss of precision is accounted for.
```bash
python remap_annotation.py
```

## Links

 - [Original images and license](https://community.brain-map.org/t/allen-human-reference-atlas-3d-2020-new/405).


## Citation

 - Ding SL, Royall JJ, ... Lein ES([2016](https://pubmed.ncbi.nlm.nih.gov/27418273/)) Comprehensive cellular-resolution atlas of the adult human brain. J Comp Neurol. 524(16):3127-481 doi: 10.1002/cne.24080
