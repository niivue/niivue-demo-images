## About

These sample NIfTI images are designed to demonstrate the [AFNI 3dAllineate](https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAllineate.html) features that are incorporated into niimath.

To use these features, your niimath needs to be from 2026 (or later) and it is recommended that you have a copy of niimath compiled for parallel processing (`OpenMP`). Both features can be detected by looking at the first output line whenever you run niimath: 

```
Chris Rorden's niimath version v1.0.20260315 OpenMP Clang17.0.0 (64-bit MacOS)
```

Here are a few example processes (assume your hardware can devote 10 CPU cores to these tasks).
 - The least-squares cost function (`-cost ls`) is the fastest, but requires the moving and stationary images are the same modality.
 - The default [Hellinger](https://en.wikipedia.org/wiki/Hellinger_distance) cost function works across modalities, but it is much slower.
 - The lpc function developed by [Saad it al.](https://pubmed.ncbi.nlm.nih.gov/18976717/) is useful for [aligning fMRI data to T1 scans](https://pubmed.ncbi.nlm.nih.gov/30361428/)
 - The `deface` function is like `allineate` except you provide a second masking image, and that image is used to mask your input image, with the input image staying in native space.
 - AFNI suggests `source_automask` for the lpc and lpa cost functions
 - The `cmass` argument uses the center of mass of the image to start a search. This can aid situations where the input image has a very different origin than the template, though it can hurt if the image includes excess neck and shoulders.
 - We also provide an [extended template for registration to images that have a lot of neck](https://nist.mni.mcgill.ca/icbm-152-extended-nonlinear-atlases-2020/). In the examples below we 

```bash
export OMP_NUM_THREADS=10
niimath T1_head -allineate MNI152_T1_1mm -cost ls ./out/wT1ls
niimath T1_head -allineate MNI152_T1_1mm ./out/wT1
niimath T1_head -allineate MNI152_T1_1mm -cmass ./out/wT1cmas
niimath fmri -allineate T1_head -cmass -cost lpc -source_automask ./out/fmri2t1
niimath T1_head -deface MNI152_T1_2mm mniMask ./out/dT1
niimath T1_head -deface MNI152_T1_2mm_ext MNI152_T1_2mm_ext_mask12 ./out/dT1_brain
niimath T1_head_ext -deface mni_icbm152_t1_tal_nlin_asym_55_ext mni_icbm152_t1_tal_nlin_asym_55_ext_mask12 -cost ls -cmass ./out/dT1_brain_ext
niimath ../CT_Philips.nii.gz  -deface mni_icbm152_t1_tal_nlin_asym_55_ext mni_icbm152_t1_tal_nlin_asym_55_ext_mask12  -cmass ./out/dCT_brain_ext
```

## Links

 - [Gao et al.](https://pubmed.ncbi.nlm.nih.gov/37293070/) note refacing methods can fail, and visual inspection is required. There subsequent work notes that even with the latest defacing or refacing, it is possible to [reconstruct faces](https://pubmed.ncbi.nlm.nih.gov/40974862/). One option may be to use the broad defacing to remove excess neck, and then conduct brain extraction with SynthStrip or mindgrab (potentially using a large dilation factor to ensure accurate homogeneity correction and measurement of CSF).
 - [3dAllineate](https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAllineate.html) notes.
 - niimath also includes `unifize` based on [3dUnifize](https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dUnifize.html) which may be useful with defacing pipelines.