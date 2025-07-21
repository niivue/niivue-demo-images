## About

Pauli and colleagues ([2018](https://pubmed.ncbi.nlm.nih.gov/29664465/)) provide a probabilistic atlas for subcortical brain nuclei. These files have been optimized for use with NiiVue and retain the original CC BY 4.0 license. A compatible NiiVue [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images) is also included. Here we use Probabilistic Atlas Quad Datatype (PAQD) encoding we describe for [other images in this repository](https://github.com/niivue/niivue-demo-images/tree/main/Thalamus).

## Creating new Atlases

This repository provides a converted atlas. For completeness, we also provide scripts to replicate and tune this process. Given the original images, you can recreate our images with these commands:

```bash
python split_left_right.py CIT168toMNI152-2009c_prob.nii.gz
python spam2paqd.py CIT168toMNI152-2009c_prob_split.nii.gz
python crop_paqd_to_rgba32.py CIT168toMNI152-2009c_prob_split_paqd.nii.gz
mv CIT168toMNI152-2009c_prob_split_paqd_cropped.nii CIT168.nii 
pigz -m -n -11 CIT168.nii 
#create meshes
python 4Datlas2mesh.py CIT168toMNI152-2009c_prob_split.nii.gz 2 0.3
python concatenatemeshes.py CIT168toMNI152-2009c_prob_split CIT168
```

The rationale for each step is as follows:
 1. split_left_right: The original atlas does not distinguish between left and right regions. This script makes a separate volume for the left and right side of each structure.
 2. spam2paqd: Convert an input 4D NIfTI image where each region to a single 3D volume with RGBA datatype. This script creates  4 volume image encoding most likely indices and probabilities.
 3. spam2paqd: convert 4-volume input into single RGBA volume, crop empty borders.
 4. 4Datlas2mesh: convert each region to a mesh. The tunable parameters are smoothing (e.g. 2mm full width half maximum) and mesh simplification (e.g. 0.3 eliminates 70% of the triangles).
 5. concatenatemeshes: create a single mesh that includes all regions.

## Links

 - [Original images and license](https://osf.io/jkzwp/).

## Citations

 - Pauli WM, Nili AN, Tyszka JM ([2018](https://pubmed.ncbi.nlm.nih.gov/29664465/)) A high-resolution probabilistic in vivo atlas of human subcortical brain nuclei. Sci Data. 5:180063. 

