# Mapping-Mountainous-Arctic-Lakes-From-the-Air
Mapping Mountainous Arctic Lake Watersheds From the Air



![alt text](AwesomeLiDAR.png)

## Clone repository and create docker cotnainer
cd /mnt/Extension_100TB/William/Projects/Abisko_lakes/code/
sudo git clone https://github.com/williamlidberg/Mapping-Mountainous-Arctic-Lakes-From-the-Air
cd /mnt/Extension_100TB/William/Projects/Abisko_lakes/code/Mapping-Mountainous-Arctic-Lakes-From-the-Air/
docker build -t abisko .
docker run -it  --mount type=bind,source=/mnt/Extension_100TB/William/Projects/Abisko_lakes/data/,target=/data --mount type=bind,source=/mnt/ramdisk/,target=/temp --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/,target=/code abisko

## Extract high resolution flow accumulation from raw DEM
python3 /code/Hydrological_processing.py /temp/ /data/aggregate2m/ /data/output/pre_processed_dem/ /data/output/flow_pointer_dir/ /data/output/flow_accumulation_dir/

## Clip flowacc to lake polygons - repair geometry first
The highest flowaccumulation within each lake polygon can be assumed to be the lake outlet. Therefore the large flow accumulation raster were clipped by each lake polygon.
python3 /code/split_flowacc_by_lake.py /temp/ /data/output/flow_accumulation_dir/dem2m.tif /data/Abisko_lakes_polygons/Abisko_lakes.shp /data/output/clipped_flowaccumulation/ 

## Find lake outlets
This script finds the maximum flow accumulation value of each lake and saves them as point shapefiles. 
python3 /code/locate_lake_outlets.py /data/output/clipped_flowaccumulation/ /data/output/outlet_points/

## Merge lake outlets

## Extract Individual watersheds
python3 code/Lake_watersheds.py /temp/ /data/aggregate2m/ /data/output/flow_pointer_dir/ /data/output/flow_accumulation_dir/ data/test_outlets.shp data/output/individual_watersheds/ data/output/watersheds_raster/


## Anaconda -python 3.8.12  
pip install whitebox==2.0.3  
conda install -c conda-forge gdal -y  
conda install geopandas -y  
conda install -c conda-forge rasterio -y

The original DEM is 15 GB and had to be split into smaller isobasins. use the following command to split the original high resolution DEM into smaller isobasins. 


## Find lake outlets
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/locate_lake_outlets.py D:/Abisko/Processing/clipped_flowaccumulation/ D:/Abisko/Processing/outlet_points/

## Extract Individual watersheds
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Lake_watersheds.py E:/Temp/ D:/Abisko/Processing/original_dem/ D:/Abisko/Processing/flow_pointer/ D:/Abisko/Processing/flow_accumulation/ D:/Abisko/test_outlets.shp D:/Abisko/Processing/individual_watersheds/ D:/Abisko/Processing/watersheds_raster/

## summary statistics
 




## old






# Extract watersheds and streams
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/National_2m_dem/ D:/temp/abisko/ --streaminitation=2500 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/

# Extract high resolution flow accumulation from original DEM
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/original_dem/ E:/Temp/ 



# Extract high resolution watersheds and streams
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/National_2m_dem/ D:/temp/abisko/ --streaminitation=2500 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/

# Run the script by giving it paths to the data
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/split_dems/ D:/temp/abisko/ --streaminitation=10000 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/






# Create isobains from the original high resolution DEM
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Create_isobasin_polygons.py D:/Abisko/original_dem/ D:/temp/abisko/ --agg_factor=16 --isobasins_size=500000 --min_area=4200000 D:/Abisko/isobasin_watersheds/


# Split the original DEM by polygon watersheds
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Split_dem.py D:/Abisko/original_dem/raw_dem.tif D:/Abisko/isobasin_watersheds/raw_dem.shp D:/temp/abisko/ D:/Abisko/split_dems/
