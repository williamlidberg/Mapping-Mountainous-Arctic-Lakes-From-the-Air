# Mapping-Mountainous-Arctic-Lakes-From-the-Air
This repository is part of a bigger project lead by Cristian Gudasz at Umeå University


![alt text](AwsomeLiDAR.png)

## Anaconda -python 3.8.12  
pip install whitebox==2.0.3  
conda install -c conda-forge gdal -y  
conda install geopandas -y  


The original DEM is 15 GB and had to be split into smaller isobasins. use the following command to split the original high resolution DEM into smaller isobasins. 

# Create isobains from the original high resolution DEM
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Create_isobasin_polygons.py D:/Abisko/original_dem/ D:/temp/abisko/ --agg_factor=16 --isobasins_size=500000 --min_area=4200000 D:/Abisko/isobasin_watersheds/watersheds.shp 

# Split the original DEM by polygon watersheds
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Split_dem.py D:/Abisko/original_dem/ D:/Abisko/isobasin_watersheds/watersheds.shp D:/temp/abisko/ D:/Abisko/split_dems/

# Run the script by giving it paths to the data
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/National_2m_dem/ D:/temp/abisko/ --streaminitation=2500 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/

python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/National_2m_dem/ D:/temp/test_raided_speed/ --streaminitation=2500 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/

