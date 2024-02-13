import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import argparse
from collections import deque

def sliding_window(granularity, window_range, data, x_grid, y_grid):


    def preload(window: list, new_y):
        for w in window: # clear everything
            w.clear()

        for x in range(window_range):
            for w in range(window_range):
                window[w].append(data[x, new_y + w]) # TODO check if this works properly
        
        return window

    # main loop

    window = [deque() for _ in range(window_range)]

    for x in x_grid:
        
        for y in y_grid:
            pass

    return

def run(granularity, length, input_shapefile, output_file_path, save_interval):
    df = pd.read_csv('../pfas_clean.csv')
    df['date'] = pd.to_datetime(df['date'])

    # filter data to points and value for testing purposes
    df_clean = df[['date', 'PFAS_total', 'longitude', 'latitude']]

    # get basin data
    file_path = input_shapefile

    # Read the zip file
    basins = gpd.read_file('zip://' + file_path)

    # Assuming your regular pandas DataFrame is df_points
    geometry = [Point(xy) for xy in zip(df_clean['longitude'], df_clean['latitude'])]
    df_points = gpd.GeoDataFrame(df_clean, geometry=geometry)
    # drop long lat, no longer needed
    df_points = df_points.drop(['longitude', 'latitude'], axis = 1)

    # groupby get latest date
    latest_date_indices = df_points.groupby('geometry')['date'].idxmax()
    df_points_unique_latest_date = df_points.loc[latest_date_indices].reset_index(drop=True)

    # we will use latest date, can change later
    # joining basins with points
    df_points_unique_latest_date.crs = 'EPSG:4326'
    basins = basins.to_crs(df_points_unique_latest_date.crs)
    result = gpd.sjoin(df_points_unique_latest_date, basins, how='right', predicate='within')

    map_boundary = result.total_bounds
    print("Map Boundary:", map_boundary)

    # Create a bounding box around area
    xmin, ymin, xmax, ymax = result.total_bounds
    x_grid = np.arange(xmin, xmax, granularity)
    y_grid = np.arange(ymin, ymax, granularity)

    print(f'x size: {len(x_grid)}, y size: {len(y_grid)}, total number of cells: {len(y_grid) * len(x_grid)}')

    grid = []
    counter = 0
    # assume number is odd
    lower_bound = length//2 * -1
    upper_bound = length//2 + 1

    print(f'range: {lower_bound, upper_bound}')

    for x in x_grid:
        for y in y_grid:
            temp = np.empty((length, length), dtype=object)
            for i in range(lower_bound, upper_bound): 
                for j in range(lower_bound, upper_bound):
                    curr_x, curr_y = x + i * granularity, y + j * granularity
                    if xmin <= curr_x <= xmax and ymin <= curr_y <= ymax: # bounds check
                        individual_point = Point(curr_x, curr_y)
                        pfas_val = 0
                        for _, basin in result.iterrows(): # search through basins
                            if individual_point.intersects(basin['geometry']):
                                pfas_val = basin['PFAS_total'] 
                                break # stop at first one
                        
                        temp[i + 3, j + 3] = {'geometry': individual_point, 'longitude': x, 'latitude': y, 'PFAS_total': pfas_val}
            
            grid.append(temp)

            counter += 1
            if counter % save_interval == 0:
                filename = "grid_data.npy"
                with open(filename, 'ab') as f:
                    np.save(f, np.array(grid))
                
                print(f'saving at {counter}')
                
                grid = []


def main():
    parser = argparse.ArgumentParser('process map data')
    parser.add_argument('-length', type=int, default=7)
    parser.add_argument('-grain', type=float, default=0.1)
    parser.add_argument('-input', type=str, default='../stanford-sr396hp9621-shapefile.zip')
    parser.add_argument('-output', type=str, default='generate.npy')
    parser.add_argument('-interval', type=int, default=100)
    
    args = parser.parse_args()
    print(args)
    # TODO check number is odd

    run(args.grain, args.length, args.input, args.output, args.interval)


if __name__ == '__main__':
    main()