# Import libraries
import geopandas as gpd
from sqlalchemy import create_engine
import overpass
import os
from dotenv import load_dotenv

# Connect to overpass API and get trails in bounding box
api = overpass.API()

bbox_coordinates = '38.50,-109.70,38.70,-109.40'

overpass_query = f"""
(
  way["highway"="track"]({bbox_coordinates});
  way["highway"="path"]({bbox_coordinates});
);
out geom;
"""

response = api.get(overpass_query)

# Parse response and set geojson to gdf, set CRS
trails_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for feature in response["features"]:
    if "geometry" in feature and feature["geometry"]["type"] == "LineString":
        trails_geojson["features"].append({
            "type": "Feature",
            "geometry": feature["geometry"],
            "properties": feature["properties"]
        })

trails_gdf = gpd.GeoDataFrame.from_features(trails_geojson["features"])
trails_gdf = trails_gdf.set_crs("EPSG:4269")
trails_gdf.head()

# Get all unique keys in tags field and set key values
all_keys = set()
trails_gdf["tags"].dropna().apply(lambda tags: all_keys.update(tags.keys()))

for key in all_keys:
    trails_gdf[key] = trails_gdf["tags"].apply(lambda tags: tags.get(key) if isinstance(tags, dict) else None)

# Send gdf to PostGIS
load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
trails_gdf.to_postgis('offroad_trails', engine, if_exists='append', index=False)