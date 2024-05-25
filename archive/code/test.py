import geopandas as gpd

gw_file_name = 'zip://GW_elevation.zip' # TODO

# Read the zip file
gw_elevation_raw = gpd.read_file(gw_file_name)
gw_elevation_raw.head()