import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point

df = pd.read_csv('pfas_clean.csv')
df['date'] = pd.to_datetime(df['date'])

# filter data to points and value for testing purposes
df_clean = df[['date', 'PFAS_total', 'longitude', 'latitude']]

# get basin data
file_path = 'stanford-sr396hp9621-shapefile.zip'

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
result = gpd.sjoin(df_points_unique_latest_date, basins, how='right', predicate='within') #

map_boundary = result.total_bounds
print("Map Boundary:", map_boundary)

# Define grid cell size in kilometers
granularity = .01 # Adjust as needed

# Create a bounding box around area
xmin, ymin, xmax, ymax = result.total_bounds
x_grid = np.arange(xmin, xmax, granularity)
y_grid = np.arange(ymin, ymax, granularity)

grid = []

for x in x_grid:
    for y in y_grid:
        temp = np.empty((7,7), dtype=object)
        for i in range(-3, 4):
            for j in range(-3, 4):
                curr_x, curr_y = x + i * granularity, y + j * granularity
                if xmin <= curr_x <= xmax and ymin <= curr_y <= ymax: # bounds check
                    individual_point = Point(curr_x, curr_y)
                    pfas_val = 0
                    for _, basin in result.iterrows(): # search through basins
                        if individual_point.intersects(basin['geometry']):
                            pfas_val = basin['PFAS_total'] 
                            break # stop at first one
                    
                    temp[i + 3, j + 3] = {'geometry': individual_point, 'longitude': x, 'latitude': y, 'PFAS_total': pfas_val}
        print(x,y)
        grid.append(temp)


grid_array = np.array(grid)

np.save('grid_array.npy', grid_array)
