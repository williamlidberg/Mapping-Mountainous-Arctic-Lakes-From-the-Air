import os
import argparse
import geopandas as gpd
from osgeo import ogr


def split_polygon(input_shape, split_shape_output):
    fn = input_shape 
    driver = ogr.GetDriverByName('ESRI Shapefile')  # See OGR Vector Format for other options
    dataSource = driver.Open(fn)
    layer = dataSource.GetLayer()
    sr = layer.GetSpatialRef()  # Spatial Reference

    dst = split_shape_output
    new_feat = ogr.Feature(layer.GetLayerDefn())  # Dummy feature

    for id, feat in enumerate(layer):
        new_ds = driver.CreateDataSource(r"{}\feat_{}.shp".format(dst, id))
        new_lyr = new_ds.CreateLayer('feat_temp_{}'.format(id), sr, ogr.wkbPolygon) 
        geom = feat.geometry().Clone()
        new_feat.SetGeometry(geom)
        new_lyr.CreateFeature(new_feat)

        del new_ds, new_lyr

def split_raster(polygon_dir, split_raster_dir):
    for polygon in polygon_dir:
        if polygon.endswith('.shp'):
            wbt.clip_raster_to_polygon(
                i = org_dem, 
                polygons = se + f, 
                output = split_dem_dir + f.replace('.shp', '.tif'), 
                maintain_dimensions=False
            )

def clean_temp(self):
    for root, dir, fs in os.walk(self.temp_dir):
        for f in fs:
            if 'temp' in f:
                os.remove(os.path.join(root, f))