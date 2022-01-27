import os
import argparse
import whitebox
import geopandas as gpd
from osgeo import ogr
wbt = whitebox.WhiteboxTools()
parser = argparse.ArgumentParser(description = 'Create isobasins and split DEM.')

class Create_isobasins:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def aggregate_dem(self, org_dem_dir, agg_factor, f):
        wbt.aggregate_raster(
            i = org_dem_dir + f, 
            output = self.temp_dir + f.replace('.tif','_aggregated_temp.tif'), 
            agg_factor = agg_factor, 
            type="mean"
        )
    def pre_process_breaching(self, f):   
        wbt.breach_depressions(
            dem = self.temp_dir + f.replace('.tif','_aggregated_temp.tif'),
            output = self.temp_dir + f.replace('.tif','_pre_processed_temp.tif'),
            max_depth=None,
            max_length=None,
            flat_increment=0.001,
            fill_pits=True
        ) 
    def create_isobasins(self, iso_size, f):
        wbt.isobasins(
            dem = self.temp_dir + f.replace('.tif','_pre_processed_temp.tif'), 
            output = self.temp_dir + f.replace('.tif','_isobasins_temp.tif'), 
            size = iso_size, 
            connections=False
        )

    def convert_raster(self, f):
        wbt.raster_to_vector_polygons(
            i = self.temp_dir + f.replace('.tif','_isobasins_temp.tif'), 
            output = self.temp_dir + f.replace('.tif','_isobasins_temp.shp')
        )       

    def calculate_attributes(self, f):
        vector_polygons = self.temp_dir + f.replace('.tif','_isobasins_temp.shp')
        # use geopandas to create area column instead of gdal
        wbt.perimeter_area_ratio(vector_polygons)
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataSource = driver.Open(vector_polygons,1) # 0 means read-only. 1 means writeable.

        if dataSource is None:
            print ('Could not open %s' % (vector_polygons))
        else:
            print ('Opened %s' % (vector_polygons))
            layer = dataSource.GetLayer()

        new_field = ogr.FieldDefn("Area", ogr.OFTReal)
        new_field.SetWidth(32)
        new_field.SetPrecision(2)
        layer.CreateField(new_field)

        for feature in layer:
            geom = feature.GetGeometryRef()
            area = geom.GetArea() 
            feature.SetField("Area", area)
            layer.SetFeature(feature)

    def delete_features(self, f, min_area, watersheds):
        vector_polygons = self.temp_dir + f.replace('.tif','_isobasins_temp.shp')
        polygons = gpd.read_file(vector_polygons)
        mask = (polygons.area > min_area)
        watershed_polygon = watersheds + f.replace('.tif','.shp')
        try:
            selected_polygons = polygons.loc[mask]
            selected_polygons.to_file(watershed_polygon)
        except:
            print(vector_polygons,'failed for some reason')

    def clean_temp(self):
            for root, dir, fs in os.walk(self.temp_dir):
                for f in fs:
                    if 'temp' in f:
                        os.remove(os.path.join(root, f))

def main(org_dem_dir, temp_dir, agg_factor, isobasins_size, min_area, watersheds):
    split = Create_isobasins(temp_dir)    
    for f in os.listdir(org_dem_dir):
        if f.endswith('.tif'):
            split.aggregate_dem(org_dem_dir, agg_factor, f)
            split.pre_process_breaching(f)
            split.create_isobasins(isobasins_size, f)
            split.convert_raster(f)
            split.calculate_attributes(f)
            split.delete_features(f, min_area, watersheds)
            #split.clean_temp(temp_dir)
            

       
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('org_dem_dir', help='Path directory of original dem')
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')
    parser.add_argument('--agg_factor', help='Aggregation factor. Default is 16 cells which is results in a 8 m DEM', type=int, default=16)
    parser.add_argument('--isobasins_size', help='Target size of isobansins in number of pixels', type=int, default=500000)
    parser.add_argument('--min_area', help='Threshold for deleting small isobasins', type=int, default=4200000)
    parser.add_argument('watersheds',help='Path to directory where final watershds will be stored')
    args = vars(parser.parse_args())
    main(**args)