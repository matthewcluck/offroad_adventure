# Import libraries
import geopandas as gpd
from sqlalchemy import create_engine
import requests
import os
from dotenv import load_dotenv

# National Parks Feature Service URL
feature_service_url = "https://mapservices.nps.gov/arcgis/rest/services/NationalDatasets/NPS_Public_POIs/FeatureServer/0"

# Set request parameters and make gdf
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "geojson"
}

response = requests.get(feature_service_url, params=params)

if response.status_code == 200:
    geojson_data = response.json()
    points_of_interest_gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    points_of_interest_gdf = points_of_interest_gdf.set_crs("EPSG:4269")
else:
    print("Failed to fetch data:", response.status_code, response.text)

# Send gdf to PostGIS
load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
points_of_interest_gdf.to_postgis('points_of_interest', engine, if_exists='append', index=False)