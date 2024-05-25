import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from shapely.ops import nearest_points
from multiprocessing import Process
import os

'''
    quick math can automate this at some point
    23500 vals
    23500 // 4 = 5875
    round down 5800, each process assign 5800, 
    23500 - (5800 * 4) = 300 vals left
'''

def combine_data(process_num, start, end, interval, input_folder, output_folder, gw_data):
    print(f'Process {process_num} starting...')
    cache = gw_data.iloc[0]
    for i in range(start, end, interval):
        raw_filename = os.path.join(input_folder, f"generate_{i}.npy")
        if os.path.exists(raw_filename):
            with open(raw_filename, 'rb') as f:
                data = np.load(f, allow_pickle=True)
                for sub in data:
                    for row in sub:
                        for item in row:
                            if item is None:
                                continue
                            long = item['longitude']
                            lat = item['latitude']
                            curr_point, elevation = Point(long, lat), 0
                            if curr_point.intersects(cache['geometry']):
                                elevation = cache['GS_Elevati']
                            else:
                                for _, gw in gw_data.iterrows(): # search through basins
                                    if curr_point.intersects(gw['geometry']):
                                        elevation = gw['GS_Elevati']
                                        cache = gw
                                        break # stop at first one
                            item['gw_elevation'] = elevation
                

                # Write modified data to a new file for this iteration
                output_filename = os.path.join(output_folder, f"cgenerate_{i}.npy")
                with open(output_filename, 'wb') as f:
                    np.save(f, data)

    print(f'Process {process_num} finished.')

def main():
    input_folder = 'data/'
    output_folder = 'cdata/'
    interval = 100
    gw_file_name = '../gw_2016.zip'

    # Read the zip file
    gw_elevation_raw = gpd.read_file('zip://' + gw_file_name)

    processes = []

    for i in range(4):
        start_idx, end_idx = i * 5800 + 100, (i + 1) * 5800 + 100
        p = Process(target=combine_data, args=(i, start_idx, end_idx, interval, input_folder, output_folder, gw_elevation_raw))
        p.start()
        processes.append(p)

    p = Process(target=combine_data, args=(4, 23300, 23600, interval, input_folder, output_folder, gw_elevation_raw))
    p.start()
    processes.append(p)

    for p in processes:
        p.join()

    print('finished full run')
    
    
        
    

    
    

if __name__ == '__main__':
    main()
