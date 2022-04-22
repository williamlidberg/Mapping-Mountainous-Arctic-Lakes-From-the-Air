from importlib.resources import path
from pathlib import Path
import pandas
import geopandas
import argparse


def main(shape_file_dir, merged_file):
    folder = Path(shape_file_dir)
    shapefiles = folder.glob('*.shp')
    gfd = pandas.concat([geopandas.read_file(shp)
    for shp in shapefiles
    ]).pipe(geopandas.GeoDataFrame)
    gdf.to_file(folder / 'merged.shp')


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Merges shapefiles in directory',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('shape_file_dir', help='path to temporary directory with shapefiles')    
    parser.add_argument('merged_file', help='path and name of merged shapefile')  
    args = vars(parser.parse_args())
    main(**args)