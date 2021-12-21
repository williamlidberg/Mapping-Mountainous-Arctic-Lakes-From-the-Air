import os
import argparse
import whitebox
wbt = whitebox.WhiteboxTools()

parser = argparse.ArgumentParser(description = 'Pre-process the DEM to make it hydrologically compatible and extract watersheds from sampling sites. ')

class Hydro_procesing:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def pre_processing(self, dem_dir, f):   
        wbt.breach_depressions(
            dem = dem_dir + f,
            output = self.temp_dir + f.replace('.tif','breached_temp.tif'),
            max_depth=None,
            max_length=None,
            flat_increment=None,
            fill_pits=False
        )

    def flow_accumulation(self, f):
        wbt.d8_pointer(
            dem = self.temp_dir + f.replace('.tif','breached_temp.tif'),
            output = self.temp_dir + f.replace('.tif','pointer_temp.tif'),
            esri_pntr=False
        )
        wbt.d8_flow_accumulation(
            i = self.temp_dir + f.replace('.tif','pointer_temp.tif'),
            output = self.temp_dir + f.replace('.tif','flowacc_temp.tif'),
            out_type="cells",
            log=False,
            clip=False,
            pntr=True,
            esri_pntr=False
        )

    def unnest_basins(self, f, streaminitation, outlets, watershed_dir):
        wbt.extract_streams(
            flow_accum = self.temp_dir + f.replace('.tif','flowacc_temp.tif'), 
            output = self.temp_dir + f.replace('.tif','streams_temp.tif'), 
            threshold = streaminitation, 
            zero_background=True
        )
        wbt.jenson_snap_pour_points(
            pour_pts = outlets, 
            streams = self.temp_dir + f.replace('.tif','streams_temp.tif'),
            output = self.temp_dir + f.replace('.tif','jenson_snapped_outlets_temp.shp'), 
            snap_dist = 20
        )
        wbt.unnest_basins(
            d8_pntr = self.temp_dir + f.replace('.tif','pointer_temp.tif'), 
            pour_pts = self.temp_dir + f.replace('.tif','jenson_snapped_outlets_temp.shp'), 
            output= self.temp_dir + f.replace('.tif','unnest_basins_temp.tif'), 
            esri_pntr=False
        ) 
        for basin in os.listdir(self.temp_dir):
            if 'unnest_basins_temp' in basin:
                wbt.raster_to_vector_polygons(
                    i = self.temp_dir + basin, 
                    output = watershed_dir + basin.replace('.tif','.shp')
                )

    def clean_temp(temp_dir):
        for root, dir, fs in os.walk(self.temp_dir):
            for f in fs:
                if 'temp' in f:
                    os.remove(os.path.join(root, f))


def main(dem_dir, temp_dir, streaminitation, outlets, watershed_dir):
    hydro = Hydro_procesing(temp_dir)    
    for f in os.listdir(dem_dir):
        if f.endswith('.tif'):
            hydro.pre_processing(dem_dir, f)
            hydro.flow_accumulation(f)
            hydro.unnest_basins(f, streaminitation, outlets, watershed_dir)
            #clean_temp(temp_dir)
        
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dem_dir', help='Path directory of dem files')
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')
    parser.add_argument('--streaminitation', help='Stream initiation threshold in number of cells. Default is 5000 cells which is 2 ha on a 1 m DEM', type=int, default=5000)
    parser.add_argument('--outlets', help='shapefile with digitised points of lake outlets')
    parser.add_argument('--watershed_dir', help='path to dir where watersheds should be stored')
    args = vars(parser.parse_args())
    main(**args)

#python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/dem/ R:/Temp/ --streaminitation=5000 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/