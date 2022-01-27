import os
import argparse
import whitebox
import geopandas as gpd
from osgeo import ogr

wbt = whitebox.WhiteboxTools()
parser = argparse.ArgumentParser(description = 'Create isobasins and split DEM.')

class Split_dem:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def split_watersheds(self, watersheds):
        fn = watersheds 
        driver = ogr.GetDriverByName('ESRI Shapefile')  # See OGR Vector Format for other options
        dataSource = driver.Open(fn)
        layer = dataSource.GetLayer()
        sr = layer.GetSpatialRef()  # Spatial Reference

        dst = self.temp_dir
        new_feat = ogr.Feature(layer.GetLayerDefn())  # Dummy feature

        for id, feat in enumerate(layer):
            new_ds = driver.CreateDataSource(r"{}\feat_{}.shp".format(dst, id))
            new_lyr = new_ds.CreateLayer('feat_temp_{}'.format(id), sr, ogr.wkbPolygon) 
            geom = feat.geometry().Clone()
            new_feat.SetGeometry(geom)
            new_lyr.CreateFeature(new_feat)

            del new_ds, new_lyr

    def split_raster(self, org_dem, f, split_dem_dir):
        wbt.clip_raster_to_polygon(
            i = org_dem, 
            polygons = self.temp_dir + f, 
            output = split_dem_dir + f.replace('.shp', '.tif'), 
            maintain_dimensions=False
        )

    def clean_temp(self):
        for root, dir, fs in os.walk(self.temp_dir):
            for f in fs:
                if 'temp' in f:
                    os.remove(os.path.join(root, f))


def main(org_dem, vector_watersheds, temp_dir, split_dem_dir):
    split = Split_dem(temp_dir)    
    split.split_watersheds(vector_watersheds)

    for f in os.listdir(temp_dir):
        if f.endswith('.shp'):
            if 'feat_' in f:
                split.split_raster(org_dem, f, split_dem_dir)
                
    #split.clean_temp(temp_dir)
            



if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('org_dem', help='Path to original dem')
    parser.add_argument('vector_watersheds', help='path to vector watersheds from SMHI or isobasins')
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')
    parser.add_argument('split_dem_dir', help='Path directory where split dem tiles will be stored')
    args = vars(parser.parse_args())
    main(**args)