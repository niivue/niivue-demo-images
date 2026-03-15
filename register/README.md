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
 - The `cmass` argument uses the center of mass of the image to start a search. This can aid situations where the input image has a very different origin than the template, though it can hurt if the image includes excess neck and shoulders.

```bash
export OMP_NUM_THREADS=10
niimath T1_head -allineate MNI152_T1_1mm -cost ls ./out/wT1ls
niimath T1_head -allineate MNI152_T1_1mm ./out/wT1
niimath fmri -allineate T1_head -cost lpc ./out/fmri2t1
niimath T1_head -deface MNI152_T1_2mm mniMask ./out/dT1
niimath T1_head -allineate MNI152_T1_1mm -cmass ./out/wT1cmas
```