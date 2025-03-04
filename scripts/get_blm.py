# Import libraries
import geopandas as gpd
from sqlalchemy import create_engine
import requests
import os
from dotenv import load_dotenv

# BLM Recreation Sites Feature Service URL
feature_service_url = "https://gis.blm.gov/utarcgis/rest/services/Recreation/BLM_UT_RECS/FeatureServer/1"

# Set request parameters and make gdf
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "geojson"
}

response = requests.get(feature_service_url, params=params)

if response.status_code == 200:
    geojson_data = response.json()
    blm_UT_recreation_gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    blm_UT_recreation_gdf = blm_UT_recreation_gdf.set_crs("EPSG:4269")
else:
    print("Failed to fetch data:", response.status_code, response.text)

# Send gdf to PostGIS
load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
blm_UT_recreation_gdf.to_postgis('blm_UT_recreation', engine, if_exists='append', index=False)