# Import libraries
import geopandas as gpd
from sqlalchemy import create_engine
import overpass
import os
from dotenv import load_dotenv

# Connect to overpass API and get fuel in bounding box
api = overpass.API()

bbox_coordinates = '38.50,-109.70,38.70,-109.40'

overpass_query = f"""
(
  way["amenity"="fuel"]({bbox_coordinates});
);
out geom;
"""

response = api.get(overpass_query)

# Parse response and set geojson to gdf, set CRS
fuel_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for feature in response["features"]:
    if "geometry" in feature:
        fuel_geojson["features"].append({
            "type": "Feature",
            "geometry": feature["geometry"],
            "properties": feature["properties"]
        })

fuel_gdf = gpd.GeoDataFrame.from_features(fuel_geojson["features"])
fuel_gdf = fuel_gdf.set_crs("EPSG:4269")
fuel_gdf.head()

# Get all unique keys in tags field and set key values
all_keys = set()
fuel_gdf["tags"].dropna().apply(lambda tags: all_keys.update(tags.keys()))

for key in all_keys:
    fuel_gdf[key] = fuel_gdf["tags"].apply(lambda tags: tags.get(key) if isinstance(tags, dict) else None)

# Send gdf to PostGIS
load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
fuel_gdf.to_postgis('moab_fuel_stations', engine, if_exists='append', index=False)