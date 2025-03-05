# Offroad Adventure

https://moabadventure.streamlit.app/

## Overview
This project is an interactive map application designed for offroad adventure enthusiasts to plan multi-day routes. The application provides geospatial data on offroad trails, fuel stations, national parks, and recreation sites, helping users navigate and plan their trips efficiently.

## Technologies
-  **Database Setup**: Data is stored in a Supabase Postgres database with PostGIS for spatial capabilities.
-  **Data Retrieval**: ESRI Feature Services and OpenStreetMap data were fetched and filtered using these Python libraries: Geopandas, Requests, and the OSM Overpass API. Sent to the database using the SQLAlchemy library.
-  **Data Cleaning**: SQL queries in PostGIS were used to filter, merge, and standardize trail data. Geopandas was also used 
-  **Application** The final dataset was converted to GeoJSON and was mapped using the Folium web mapping library, and hosted using the Streamlit API.

## Data Sources
- **Trails**: Extracted from OpenStreetMap using Overpass API.
- **Gas Stations**: Extracted from OpenStreetMap using Overpass API.
- **National Parks**: Obtained from the National Park Service. https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_National_Park_Service_Lands_20170930/FeatureServer/0
- **BLM Recreation Sites**: Collected from the Bureau of Land Management. https://gis.blm.gov/utarcgis/rest/services/Recreation/BLM_UT_RECS/FeatureServer/1

## Future Improvements
- Add more datasets such as amenities
- Add more attribute data to the trails
- Improve folium map UI and interactivity
- Improve overall website UI
- Fix authentication issues with Streamlit and my Supabase so data is hosted dynamically

