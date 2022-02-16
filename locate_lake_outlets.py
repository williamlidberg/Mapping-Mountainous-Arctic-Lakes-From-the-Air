import os
import argparse
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

parser = argparse.ArgumentParser(description = 'Find lake outlet by creating a point at the highest flow accumulation value.')

def find_outlet(watershed, f, outlet_dir):
    flowaccumulation = watershed + f
    with rasterio.open(flowaccumulation, 'r') as ras:
        arr = ras.read(1)
        high_point = np.amax(arr)
        res = np.where(arr == np.amax(arr))
        highest = ras.xy(res[0], res[1])
        point_coord = Point(highest[0][0], highest[1][0])
        df = {'flowacc': [high_point], 'geometry': [point_coord]}
        point = gpd.GeoDataFrame(df, geometry='geometry', crs ="EPSG:3006")
        point.to_file(outlet_dir + f.replace('.tif','.shp'))
        print('Located outlet for', f)


def main(flowaccumulation_dir, outlet_dir):
    for f in os.listdir(flowaccumulation_dir):
        if f.endswith('.tif'):
            find_outlet(flowaccumulation_dir, f, outlet_dir)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('flowaccumulation_dir', help='Path to directory with flow accumulation rasters')
    parser.add_argument('outlet_dir', help='path to directory where lake outlets will be stored')

    args = vars(parser.parse_args())
    main(**args)