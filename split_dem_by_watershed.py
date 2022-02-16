import os
import argparse
import whitebox
wbt = whitebox.WhiteboxTools()

parser = argparse.ArgumentParser(description = 'Pre-process the DEM to make it hydrologically compatible and extract watersheds from sampling sites. ')


class watersheds:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def create_watersheds(self,outlet_dir, f, flow_pointer, dem, watershed_dir, watershed_dem_dir):
#        wbt.snap_pour_points(
#            pour_pts = f, 
#            flow_accum = self.temp_dir + f.replace('.tif','_flowacc_temp.tif'), 
#            output = self.temp_dir + f.replace('.tif','_snapped_outlets_temp.shp'), 
#            snap_dist = 1 # outlets were created from the coordinate of the highest flow accumulation cell. so we only move it slightly to make sure it matches whitebox coordinates.
#        )
        wbt.watershed(
            d8_pntr = flow_pointer, 
            pour_pts = outlet_dir + f, 
            output = self.temp_dir + f.replace('.shp','_watershed_temp.tif'), 
            esri_pntr=False
        )
        wbt.raster_to_vector_polygons(
            i = self.temp_dir + f.replace('.shp','_watershed_temp.tif'), 
            output = watershed_dir + f
        )
        wbt.clip_raster_to_polygon(
            i = dem, 
            polygons = watershed_dir + f, 
            output = watershed_dem_dir + f.replace('.shp', '.tif'), 
            maintain_dimensions=False
        )


def main(temp_dir, flow_pointer, dem, outlet_dir, watershed_dir, watershed_dem_dir):
    watershed = watersheds(temp_dir)    
    for f in os.listdir(outlet_dir):
        if f.endswith('.shp'):
            watershed.create_watersheds(outlet_dir,f, flow_pointer, dem, watershed_dir, watershed_dem_dir)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')
    parser.add_argument('flow_pointer', help='path to large flow pointer raster to use for watershed creation')
    parser.add_argument('dem', help='Path to large dem')
    parser.add_argument('outlet_dir', help='path to directory where outlets points are stored')
    parser.add_argument('watershed_dir', help='path to directory where watersheds will be saved')
    parser.add_argument('watershed_dem_dir', help='path to diretory where dems shaped liked watersheds will be saved')
    args = vars(parser.parse_args())
    main(**args)