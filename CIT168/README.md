## About

Pauli and colleagues ([2018](https://pubmed.ncbi.nlm.nih.gov/29664465/)) provide a probabilistic atlas for subcortical brain nuclei. These files have been optimized for use with NiiVue and retain the original CC BY 4.0 license. A compatible NiiVue [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images) is also included. Here we use Sparse Probabilistic Atlas with Ranked Quad (SPARQ) encoding we describe for [other images in this repository](https://github.com/niivue/niivue-demo-images/tree/main/Thalamus).

## Creating new Atlases

The provided Python scripts can convert a probabilistic atlas to SPARQ. For example, to convert the original images you can run:

```bash
python spam2sparq.py CIT168toMNI152-2009c_prob.nii.gz
python crop_sparq_to_rgba32.py CIT168toMNI152-2009c_prob.nii.gz
```

## Links

 - [Original images and license](https://osf.io/jkzwp/).

## Citations

 - Pauli WM, Nili AN, Tyszka JM ([2018](https://pubmed.ncbi.nlm.nih.gov/29664465/)) A high-resolution probabilistic in vivo atlas of human subcortical brain nuclei. Sci Data. 5:180063. 

