## About

Xiao et al. ([2017](https://pubmed.ncbi.nlm.nih.gov/28491942/) provide a spatial probabilistic atlas map (SPAM) of subcortical structures based on images from 25 individuals with Parkinson׳s disease (PD). While the template and atlas are approximately aligned to MNI space, it captures general features of this population (e.g. dilated ventricles relative to templates from young healthy adults). The orignal images include templates in different modalities, but here we provide the T1-T2* fusion which provides good contrast for subcortical structures. These files have been optimized for use with NiiVue and retain the original CC BY-NC-SA 3.0 license. A compatible NiiVue [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images) is also included. Images have been losslessly cropped and precision down-sampled to reduce file size.

## Creating new Atlases

While we provide processed files, we also include Python scripts that can be adapted for other templates and atlases.

```bash
nii=PD25-fusion-template-1mm
niimath mni_icbm152_t1_tal_nlin_asym_09c_mask -s 2 -thr 0.1 -s 1 smask
niimath smask -reslice ${nii} rsmask
niimath ${nii} -mul rsmask -scale01 -mul 255 b$nii -odt char
python crop_zeros.py b${nii}.nii.gz
```

## Links

 - [Original images and license](https://nist.mni.mcgill.ca/multi-contrast-pd25-atlas/).

## Citations

 - Xiao Y, Fonov V, Chakravarty MM, Beriault S, Al Subaie F, Sadikot A, Pike GB, Bertrand G, Collins DL  ([2017](https://pubmed.ncbi.nlm.nih.gov/28491942/)) A dataset of multi-contrast population-averaged brain MRI atlases of a Parkinson׳s disease cohort
Data Brief
