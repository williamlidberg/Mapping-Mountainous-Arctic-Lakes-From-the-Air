import os
import argparse
import whitebox
wbt = whitebox.WhiteboxTools()

parser = argparse.ArgumentParser(description = 'Pre-process the DEM to make it hydrologically compatible and extract flow pointer and flow accumulation rasters. ')

class Hydro_procesing:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    def pre_process_breaching(self,f, dem_dir, correct_dem):   
        wbt.breach_depressions(
            dem = dem_dir + f,
            output = correct_dem + f,
            max_depth=None,
            max_length=None,
            flat_increment=0.01,
            fill_pits=True
        )
    def flow_accumulation(self, f, correct_dem, flow_pointer_dir, flow_accumulation_dir):
        wbt.d8_pointer(
            dem = correct_dem + f,
            output = flow_pointer_dir + f,
            esri_pntr=False
        )
        wbt.d8_flow_accumulation(
            i = flow_pointer_dir + f,
            output = flow_accumulation_dir + f,
            out_type='catchment area',
            log=False,
            clip=False,
            pntr=True,
            esri_pntr=False
        )

    #add additional optimal functions later

def main(dem_dir, temp_dir, correct_dem_dir, flow_pointer_dir, flow_accumulation_dir):
    hydro = Hydro_procesing(temp_dir)    
    for f in os.listdir(dem_dir):
        if f.endswith('.tif'):
            hydro.pre_process_breaching(f, dem_dir, correct_dem_dir)
            hydro.flow_accumulation(f, correct_dem_dir, flow_pointer_dir, flow_accumulation_dir)

       
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')    
    parser.add_argument('dem_dir', help='Path directory of dem files')  
    parser.add_argument('correct_dem_dir', help='Path to directory where the Hydrologically correct dem will be saved')
    parser.add_argument('flow_pointer_dir', help='Path to directory where the flow pointer will be saved')
    parser.add_argument('flow_accumulation_dir', help='Path to directory where the flow accumulation will be saved')
    args = vars(parser.parse_args())
    main(**args)