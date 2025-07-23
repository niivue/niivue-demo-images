## About

Nettekoven et al. ([2024](https://pubmed.ncbi.nlm.nih.gov/39333089/)) provide a spatial probabilistic atlas map (SPAM) for cerebellar regions are hierarchically organized across three levels. These files have been optimized for use with NiiVue, maintaining the [CC BY-ND licence](https://www.diedrichsenlab.org/imaging/atlasPackage.htm). Specifically, file size is reduced by convertint the atlas to Probabilistic Atlas Quad Datatype (PAQD) and a compatible NiiVue [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images). The PAQD encoding is [described here](https://github.com/niivue/niivue-demo-images/tree/main/Thalamus).

## Creating new Atlases

The provided Python script can convert a probabilistic atlas to PAQD. For example, if for the [Cerebellum-MNIfnirt-prob-1mm](https://web.mit.edu/fsl_v5.0.10/fsl/doc/wiki/Atlases.html) you can run:

```bash
python spam2paqd.py atl-NettekovenAsym32_space-MNI152NLin6AsymC_probseg.nii.gz
python crop_paqd_to_rgba32.py atl-NettekovenAsym32_space-MNI152NLin6AsymC_probseg_paqd.nii.gz
pigz -m -n -11 atl-NettekovenAsym32_space-MNI152NLin6AsymC_probseg_paqd_cropped.nii
```

## Links

 - [License](https://www.diedrichsenlab.org/imaging/atlasPackage.htm) and [original images](https://github.com/diedrichsenlab/cerebellar_atlases).

## Citations

 - Nettekoven C, Zhi D, Shahshahani L, Pinho AL, Saadon-Grosman N, Buckner RL, Diedrichsen J ([2024](https://pubmed.ncbi.nlm.nih.gov/39333089/)) A hierarchical atlas of the human cerebellum for functional precision mapping. Nat Commun. DOI: 10.1038/s41467-024-52371-w