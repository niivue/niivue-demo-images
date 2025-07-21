Here are a few pre-processing scripts:
 1. extract "gray value" and "name: from XML and label from CSV, save results in lined_output.csv
 2. julich2paqd.py convert all  probabilisticNIfTI images to single 4-volume PAQD
 3. crop_paqd_to_rgba32.py crop PAQD and save as 1-volume RGBA
 4. linked_output2cmap.py create a colormap
 
```
python xml2csv.py
python julich2paqd.py linked_output.csv ./probabilistic-maps_PMs_207-areas
python julich2paqd.py linked_output.csv ./probabilistic-maps_PMs_207-areas rh
python crop_paqd_to_rgba32.py probabilistic-maps_PMs_207-areas_rh_paqd.nii.gz
python crop_paqd_to_rgba32.py probabilistic-maps_PMs_207-areas_lh_paqd.nii.gz
python linked_output2cmap.py
```