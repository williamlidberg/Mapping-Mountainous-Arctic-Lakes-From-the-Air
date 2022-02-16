import os
import argparse
import geopandas as gpd
from osgeo import ogr
import whitebox

wbt = whitebox.WhiteboxTools()

parser = argparse.ArgumentParser(description = 'Find outlets of each lake.')

class Split:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def split_watersheds(self, lake_polygons):
        fn = lake_polygons 
        driver = ogr.GetDriverByName('ESRI Shapefile')  # See OGR Vector Format for other options
        dataSource = driver.Open(fn)
        layer = dataSource.GetLayer()
        sr = layer.GetSpatialRef()  # Spatial Reference
        dst = self.temp_dir
        new_feat = ogr.Feature(layer.GetLayerDefn())  # Dummy feature

        for id, feat in enumerate(layer):
            new_ds = driver.CreateDataSource(r"{}\feat_{}.shp".format(dst, id))
            new_lyr = new_ds.CreateLayer('lake_temp_{}'.format(id), sr, ogr.wkbPolygon) 
            geom = feat.geometry().Clone()
            new_feat.SetGeometry(geom)
            new_lyr.CreateFeature(new_feat)
            

            del new_ds, new_lyr

    def split_raster(self, flow_accumulation, f, clipped_lakes_dir):
        wbt.clip_raster_to_polygon(
            i = flow_accumulation, 
            polygons = self.temp_dir + f, 
            output = clipped_lakes_dir + f.replace('.shp', '.tif'), 
            maintain_dimensions=False
        )

    def clean_temp(self):
        for root, dir, fs in os.walk(self.temp_dir):
            for f in fs:
                if 'feat' in f:
                    os.remove(os.path.join(root, f))

def main(temp_dir, flow_accumulation, lake_polygons, clipped_lakes_dir):
    split = Split(temp_dir)    
    split.split_watersheds(lake_polygons)
    print('split complete')
    for f in os.listdir(temp_dir):
        if f.endswith('.shp'):
            if 'feat_' in f:
                split.split_raster(flow_accumulation, f, clipped_lakes_dir)       
    split.clean_temp()

if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('temp_dir', help='path to temporary directory')
    parser.add_argument('flow_accumulation', help='Path to flow accumulation raster to be clipped')
    parser.add_argument('lake_polygons', help='path to vector watersheds from SMHI or isobasins')
    parser.add_argument('clipped_lakes_dir', help='Path directory where split dem tiles will be saved')
    args = vars(parser.parse_args())
    main(**args)