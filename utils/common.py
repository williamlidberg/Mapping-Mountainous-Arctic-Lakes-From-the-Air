import os
import whitebox
import geopandas as gpd
from osgeo import ogr
wbt = whitebox.WhiteboxTools()

class common:
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

