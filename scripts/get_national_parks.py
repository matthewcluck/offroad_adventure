# Import libraries
import geopandas as gpd
from sqlalchemy import create_engine
import requests
import os
from dotenv import load_dotenv

# National Parks Feature Service URL
feature_service_url = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_National_Park_Service_Lands_20170930/FeatureServer/0/query"

# Set request parameters and make gdf
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "geojson"
}

response = requests.get(feature_service_url, params=params)

if response.status_code == 200:
    geojson_data = response.json()
    national_parks_gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    national_parks_gdf = national_parks_gdf.set_crs("EPSG:4269")
else:
    print("Failed to fetch data:", response.status_code, response.text)

# Send gdf to PostGIS
load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
national_parks_gdf.to_postgis('national_parks', engine, if_exists='append', index=False)