import os
import argparse
from tempfile import tempdir
from osgeo import ogr
import whitebox
wbt = whitebox.WhiteboxTools()

parser = argparse.ArgumentParser(description = 'Pre-process the DEM to make it hydrologically compatible and extract watersheds from sampling sites. ')


class watersheds:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def unnest_basins(self, f, d8_pointer, d8_flowacc, merged_outlets):      
        wbt.snap_pour_points(
            pour_pts = merged_outlets, 
            flow_accum = d8_flowacc + f, 
            output = self.temp_dir + 'temp_snapped.shp', 
            snap_dist = 10
        )
        print('snapped pout points with 10m')
        wbt.unnest_basins(
            d8_pntr = d8_pointer + f, 
            pour_pts = self.temp_dir + 'temp_snapped.shp', 
            output= self.temp_dir + '_unnest_basins' + f, 
            esri_pntr=False
        ) 
        for basin in os.listdir(self.temp_dir):
            if '_unnest_basins' in basin and basin.endswith('.tif'):
                wbt.raster_to_vector_polygons(
                    i = self.temp_dir + basin, 
                    output = self.temp_dir + basin.replace('.tif','.shp')
                )

    def split_polygon(self, split_shape_output):
        for watershed in os.listdir(self.temp_dir):
            if watershed.endswith('.shp') and '_unnest_basins' in watershed:
                print(watershed)
                fn = self.temp_dir + watershed
                driver = ogr.GetDriverByName('ESRI Shapefile')  # See OGR Vector Format for other options
                dataSource = driver.Open(fn)
                layer = dataSource.GetLayer()
                sr = layer.GetSpatialRef()  # Spatial Reference
                dst = split_shape_output
                new_feat = ogr.Feature(layer.GetLayerDefn())  # Dummy feature

                for id, feat in enumerate(layer):
                    new_ds = driver.CreateDataSource(r"{}\feat_{}.shp".format(dst, id))
                    new_lyr = new_ds.CreateLayer('watershed_{}'.format(id), sr, ogr.wkbPolygon) 
                    geom = feat.geometry().Clone()
                    new_feat.SetGeometry(geom)
                    new_lyr.CreateFeature(new_feat)
                    del new_ds, new_lyr

    def split_raster(self, dem_dir, f, individual_watersheds_dir, split_raster_dir):
        for polygon in os.listdir(individual_watersheds_dir):
            if polygon.endswith('.shp'):
                wbt.clip_raster_to_polygon(
                    i = dem_dir + f, 
                    polygons = individual_watersheds_dir + polygon, 
                    output = split_raster_dir + polygon.replace('.shp', '.tif'), 
                    maintain_dimensions=False
                )
    def clean_temp(self):
            for root, dir, fs in os.walk(self.temp_dir):
                for f in fs:
                    if '_unnest_basins' in f:
                        os.remove(os.path.join(root, f))

def main(temp_dir, dem_dir, d8_pointer, d8_flowacc, merged_outlets, individual_watersheds_dir, split_raster_dir):
    watershed = watersheds(temp_dir)
    for f in os.listdir(dem_dir):
        if f.endswith('.tif'):
            watershed.unnest_basins(f, d8_pointer, d8_flowacc, merged_outlets)
            watershed.split_polygon(individual_watersheds_dir)
            #watershed.split_raster(dem_dir, f, individual_watersheds_dir, split_raster_dir)
            watershed.clean_temp()



if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')
    parser.add_argument('dem_dir', help='Path directory of demfile')
    parser.add_argument('d8_pointer', help='Path to directory of d8_file')
    parser.add_argument('d8_flowacc', help='Path to directory of d8_flowacc')
    parser.add_argument('merged_outlets', help='shapefile with digitised points of lake outlets')
    parser.add_argument('individual_watersheds_dir', help='Path to dir where individual_watersheds_dir')
    parser.add_argument('split_raster_dir', help='path to dir where split rasters will be stored')
    args = vars(parser.parse_args())
    main(**args)