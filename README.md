# Mapping-Mountainous-Arctic-Lakes-From-the-Air
Mapping Mountainous Arctic Lake Watersheds From the Air


![alt text](AwesomeLiDAR.png)

## Anaconda -python 3.8.12  
**Not sure whats going on with h5py, will fix in container later**   
pip install whitebox==2.0.3  
conda install -c conda-forge gdal -y  
conda install geopandas -y  


The original DEM is 15 GB and had to be split into smaller isobasins. use the following command to split the original high resolution DEM into smaller isobasins. 

# Create isobains from the original high resolution DEM
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Create_isobasin_polygons.py D:/Abisko/original_dem/ D:/temp/abisko/ --agg_factor=16 --isobasins_size=500000 --min_area=4200000 D:/Abisko/isobasin_watersheds/

# Split the original DEM by polygon watersheds
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Split_dem.py D:/Abisko/original_dem/orgdem.tif D:/Abisko/isobasin_watersheds/watersheds.shp D:/temp/abisko/ D:/Abisko/split_dems/

# Extract high resolution watersheds and streams
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/National_2m_dem/ D:/temp/abisko/ --streaminitation=2500 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/
