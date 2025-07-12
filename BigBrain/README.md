## About

The BigBrain Atlas provides subcortical segmentations for 22 nuclei developed by Xiao and colleagues. The files here have been optimized for use with NiiVue, while retaining the same [CC BY 4.0 License](https://osf.io/xkqb3/). Specifically, a [colormap](https://niivue.com/docs/colormaps2#atlases-and-labeled-images) is provided that uses the same color scheme as FreeSurfer. The voxel-based images have been losslessly cropped from 394×466×378 to 310×374×317, and the data type has been converted from float32 to uint8.

## Creating new Atlases

The converted atlases are provided, but Python scripts are also available to generate meshes directly from a labeled NIfTI image to a [mz3 format mesh](https://github.com/neurolabusc/surf-ice/tree/master/mz3). These scripts extend the functionality of [earlier Python](https://github.com/rordenlab/pythonScripts/tree/main/atlas2mz3) and [Matlab](https://github.com/neurolabusc/surfice_atlas) scripts. The atlas2mesh.py script takes a NIfTI atlas where voxel intensities represent integer region labels. It accepts two optional parameters: (1) a Gaussian blur (in mm FWHM), which reduces jagged edges at the cost of smoothing sharp features, and (2) a mesh simplification ratio, where 1.0 preserves the original geometry and smaller values reduce file size by decimating the mesh. For example, using a 5 mm blur and a simplification factor of 0.3 creates smoother, smaller meshes. The concatenatemeshes.py script then merges these individual meshes into a single file, embedding region metadata and a colormap from an accompanying JSON file. The final .mz3 mesh was generated using this workflow:

```bash
python atlas2mesh.py bigbrain.nii.gz 5 0.3
python concatenatemeshes.py bigbrain
```

## Links

 - [Original images and license](https://osf.io/xkqb3/).
 - [earlier Python scripts](https://github.com/rordenlab/pythonScripts/tree/main/atlas2mz3)
 - [earlier Matlab scripts](https://github.com/neurolabusc/surfice_atlas)
 - [mz3 format mesh](https://github.com/neurolabusc/surf-ice/tree/master/mz3)

## Citation

 - Xiao Y, Lau JC, Anderson T, DeKraker J, Collins DL, Peters T, Khan AR ([2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6797784/)) An accurate registration of the BigBrain dataset with the MNI PD25 and ICBM152 atlases. Sci Data. 6:210. doi: 10.1038/s41597-019-0217-0
