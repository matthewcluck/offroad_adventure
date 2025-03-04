import geopandas as gpd
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
# Connect to postgis database
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
sql_query_trails = 'SELECT * FROM moab_offroad_trails'
sql_query_national_parks = "SELECT * FROM national_parks WHERE unit_name = 'Arches National Park'"
sql_query_fuel = "SELECT * FROM moab_fuel_stations"
sql_points_of_interest = "SELECT * FROM points_of_interest"
sql_blm = "SELECT * FROM blm_ut_rec_sites"
sql_starts_ends = "SELECT * FROM starts_ends"

moab_offroad_trails_gdf = gpd.read_postgis(sql_query_trails, con=DATABASE_URL, geom_col='combined_geometry')
national_parks_gdf = gpd.read_postgis(sql_query_national_parks, con=DATABASE_URL, geom_col='geometry')
moab_fuel_stations_gdf = gpd.read_postgis(sql_query_fuel, con=DATABASE_URL, geom_col='geometry')
#points_of_interest_gdf = gpd.read_postgis(sql_points_of_interest , con=DATABASE_URL, geom_col='geometry')
blm_gdf = gpd.read_postgis(sql_blm , con=DATABASE_URL, geom_col='geometry')
starts_ends_gdf = gpd.read_postgis(sql_starts_ends , con=DATABASE_URL, geom_col='geom')

# Filter trails by day
day_1_trail_names = ["Slickrock", "Slickrock Cutoff", "Slickrock Alternate", "Staircase", "Hell's Revenge 4x4 Trail"]
day_1_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_1_trail_names)]

day_2_trail_names = ["Poison Spider", "Golden Spike", "Portal Trail"]
day_2_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_2_trail_names)]

day_3_trail_names = ["Little Canyon", "Great Escape", "Arth's Corner", "Bull Canyon Road", "Rusty Nail", "Gold Bar Rim"]
day_3_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_3_trail_names)]

# Download files to geojson
national_parks_gdf.to_file("national_parks.geojson", driver="GeoJSON")
moab_fuel_stations_gdf.to_file("moab_fuel_stations.geojson", driver="GeoJSON")
blm_gdf.to_file("blm.geojson", driver="GeoJSON")
starts_ends_gdf.to_file("starts_ends.geojson", driver="GeoJSON")

day_1_trails.to_file("day_1_trails.geojson", driver="GeoJSON")
day_2_trails.to_file("day_2_trails.geojson", driver="GeoJSON")
day_3_trails.to_file("day_3_trails.geojson", driver="GeoJSON")