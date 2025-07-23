## About

Diedrichsen and colleagues ([2009](https://pubmed.ncbi.nlm.nih.gov/19457380/)) provide a spatial probabilistic atlas map (SPAM) for cerebellar regions. These files have been optimized for use with NiiVue, maintaining the [CC BY-ND licence](https://www.diedrichsenlab.org/imaging/atlasPackage.htm). Specifically, file size is reduced by converting the atlas to Probabilistic Atlas Quad Datatype (PAQD) and a compatible NiiVue [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images). The PAQD encoding is [described here](https://github.com/niivue/niivue-demo-images/tree/main/Thalamus).

## Creating new Atlases

The provided Python script can convert a probabilistic atlas to PAQD. For example, if for the [Cerebellum-MNIfnirt-prob-1mm](https://web.mit.edu/fsl_v5.0.10/fsl/doc/wiki/Atlases.html) you can run:

```bash
python spam2paqd.py atl-Anatom_space-MNI_probseg.nii
python crop_paqd_to_rgba32.py atl-Anatom_space-MNI_probseg_paqd.nii.gz
pigz -m -n -11 atl-Anatom_space-MNI_probseg_paqd_cropped.nii
mv atl-Anatom_space-MNI_probseg_paqd_cropped.nii.gz atl-Anatom.nii.gz
python lut2cmap.py  
```

## Links

 - [License](https://www.diedrichsenlab.org/imaging/atlasPackage.htm) and [original images](https://github.com/diedrichsenlab/cerebellar_atlases).

## Citations

 - Diedrichsen J, Balsters JH, Flavell J, Cussans E, Ramnani N ([2009](https://pubmed.ncbi.nlm.nih.gov/19457380/)) A probabilistic MR atlas of the human cerebellum. Neuroimage. DOI: 10.1016/j.neuroimage.2009.01.045
