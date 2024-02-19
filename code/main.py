import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import argparse
from collections import deque

class GenerateShape:
    def __init__(self, granularity, length, save_interval, checkpoint, output_file):
        self.granularity = granularity
        self.length = length
        self.save_interval = save_interval
        self.output_file = output_file
        self.base = None
        self.checkpoint = checkpoint

    def run(self):
        '''
        take overlayed image and generates squares for ML
        '''
        xmin, ymin, xmax, ymax = self.base.total_bounds
        x_grid = np.arange(xmin, xmax, self.granularity)
        y_grid = np.arange(ymin, ymax, self.granularity)

        print(f'x size: {len(x_grid)}, y size: {len(y_grid)}, total number of cells: {len(y_grid) * len(x_grid)}')

        # assume number is odd
        lower_bound = self.length//2 * -1
        upper_bound = self.length//2 + 1

        print(f'range: {lower_bound, upper_bound}')
        print('starting run...')

        counter = 0
        grid = []
        cache = self.base.iloc[0]

        for x in x_grid:
            for y in y_grid:
                if self.checkpoint > counter: # checkpointing
                    counter += 1
                    continue
                curr = np.empty((self.length, self.length), dtype=object)
                for i in range(self.length):
                    for j in range(self.length):
                        curr_x, curr_y = x + i * self.granularity, y + j * self.granularity
                        if xmin <= curr_x <= xmax and ymin <= curr_y <= ymax: # bounds check
                            curr_point, pfas_val = Point(curr_x, curr_y), 0
                            if curr_point.intersects(cache['geometry']):
                                pfas_val = ['PFAS_total']
                            else:
                                for _, basin in self.base.iterrows(): # search through basins
                                    if curr_point.intersects(basin['geometry']):
                                        pfas_val = basin['PFAS_total'] 
                                        cache = basin
                                        break # stop at first one
                            curr[i, j] = {'longitude': x, 'latitude' : y, 'pfas': pfas_val}
                grid.append(curr)

                # save here
                if counter % self.save_interval == 0:
                    with open(self.output_file, 'ab') as f:
                        np.save(f, np.array(grid)) # save here
                    print(f'saved at {counter}')
                    grid = []
                counter += 1
        
        print('finished run')
        

    def setup(self, input_shapefile, csv):
        df = pd.read_csv(csv)
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
        self.base = result
        print('finished setup')
        
def main():
    parser = argparse.ArgumentParser('process map data')
    parser.add_argument('-length', type=int, default=7)
    parser.add_argument('-grain', type=float, default=0.1)
    parser.add_argument('-input', type=str, default='../stanford-sr396hp9621-shapefile.zip')
    parser.add_argument('-csv', type=str, default='../pfas_clean.csv')
    parser.add_argument('-output', type=str, default='generate.npy')
    parser.add_argument('-interval', type=int, default=10)
    parser.add_argument('-checkpoint', type=int, default=0)
    
    args = parser.parse_args()
    print(args)
    # TODO check number is odd

    x = GenerateShape(args.grain, args.length, args.interval, args.checkpoint, args.output)
    x.setup(args.input, args.csv)
    x.run()


if __name__ == '__main__':
    main()