import os
import argparse
import whitebox
import geopandas as gpd
from osgeo import ogr
import utils.Split_dem

parser = argparse.ArgumentParser(description = 'Find outlets of each lake.')

#split lake _Polygon 
#find three maximum flow acc CellT
#convert to point shapefile
#extract watersheds


def main(flow_accumulation, lake_polygons, temp_dir, clip_flowacc):
    #split_watersheds(lake_polygons, temp_dir)

    split = utils.Split_dem.Split(temp_dir)    
    split.split_watersheds(lake_polygons)

    for f in os.listdir(temp_dir):
        if f.endswith('.shp'):
            if 'feat_' in f:
                split.split_raster(flow_accumulation, f, clip_flowacc)       



if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('flow_accumulation', help='Path to original dem')
    parser.add_argument('lake_polygons', help='path to vector watersheds from SMHI or isobasins')
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')
    parser.add_argument('clip_flowacc', help='Path directory where split dem tiles will be stored')
    args = vars(parser.parse_args())
    main(**args)