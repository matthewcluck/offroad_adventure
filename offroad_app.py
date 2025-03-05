import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv

# Set streamlit app styles and title
st.markdown("""
    <style>

        body {
            background-color: #f8f8f8 !important;  /* Off-white color */
        }

        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        #map_div {
            width: 100% !important;
            max-width: 1200px !important;
            max-height: 900px !important;
            border: 10px solid black;
        }
            
        .stMainBlockContainer.block-container {
            padding: 20px !important;
        }

    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>Moab 3 Day Offroad Adventure Guide</h1>", unsafe_allow_html=True)

# Function to read in geojson from github
@st.cache_data
def load_geojson():
    day_1_trails_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/day_1_trails.geojson"
    day_2_trails_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/day_2_trails.geojson"
    day_3_trails_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/day_3_trails.geojson"
    national_parks_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/national_parks.geojson"
    moab_fuel_stations_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/moab_fuel_stations.geojson"
    blm_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/blm.geojson"
    starts_ends_url = "https://raw.githubusercontent.com/matthewcluck/offroad_adventure/refs/heads/main/geojson/starts_ends.geojson"
    
    day_1_trails = gpd.read_file(day_1_trails_url)
    day_2_trails = gpd.read_file(day_2_trails_url)
    day_3_trails = gpd.read_file(day_3_trails_url)
    national_parks_gdf = gpd.read_file(national_parks_url)
    moab_fuel_stations_gdf = gpd.read_file(moab_fuel_stations_url)
    blm_gdf = gpd.read_file(blm_url)
    starts_ends_gdf = gpd.read_file(starts_ends_url)

    return day_1_trails, day_2_trails, day_3_trails, national_parks_gdf, moab_fuel_stations_gdf, blm_gdf, starts_ends_gdf

# Load the data as gdf
day_1_trails, day_2_trails, day_3_trails, national_parks_gdf, moab_fuel_stations_gdf, blm_gdf, starts_ends_gdf = load_geojson()

m = folium.Map(location=[38.60, -109.58], zoom_start=12, control_scale=True)

# Adding all layers to map
folium.GeoJson(
    blm_gdf,
    name="BLM Recreation Sites",
    tooltip=folium.GeoJsonTooltip(fields=["BLM Rec Site"]),
    style_function=lambda feature: {
        "fillColor": "gray",
        "color": "gray",
        "weight": 1,
        "fillOpacity": 0.1
    }
).add_to(m)

folium.GeoJson(
    day_1_trails,
    name="Day 1 Trails",
    tooltip=folium.GeoJsonTooltip(fields=["name"]),
    popup=folium.GeoJsonPopup(fields=["name", "surface", "length_miles"]),
    style_function=lambda feature: {"color": "purple", "weight": 5}
).add_to(m)

folium.GeoJson(
    day_2_trails,
    name="Day 2 Trails",
    tooltip=folium.GeoJsonTooltip(fields=["name"]),
    popup=folium.GeoJsonPopup(fields=["name", "surface", "length_miles"]),
    style_function=lambda feature: {"color": "yellow", "weight": 5}
).add_to(m)

folium.GeoJson(
    day_3_trails,
    name="Day 3 Trails",
    tooltip=folium.GeoJsonTooltip(fields=["name"]),
    popup=folium.GeoJsonPopup(fields=["name", "surface", "length_miles"]),
    style_function=lambda feature: {"color": "orange", "weight": 5}
).add_to(m)

national_parks_gdf["Info"] = "Arches National Park: No offroading allowed."

folium.GeoJson(
    national_parks_gdf,
    name="National Parks",
    tooltip=folium.GeoJsonTooltip(fields=["Info"]),
    style_function=lambda feature: {
        "fillColor": "red",
        "color": "red",
        "weight": 1,
        "fillOpacity": 0.1
    }
).add_to(m)

folium.GeoJson(
    moab_fuel_stations_gdf,
    name="Gas Stations",
    popup=folium.GeoJsonPopup(fields=["brand", "addr:housenumber", "addr:street"]),
    style_function=lambda feature: {
        "fillColor": "black",
        "color": "black",
        "weight": 6
    }
).add_to(m)

for _, row in starts_ends_gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=8,
        color='brown',
        fill=True,
        fill_color='brown',
        fill_opacity=0.6,
        popup=row['Info']
    ).add_to(m)

folium.LayerControl().add_to(m)

# Arrange page elements
col1, col2, col3 = st.columns([2, 9, 2])

# Define the legend HTML to be displayed in the second column
legend_html = '''
    <div style="background-color: lightgray; border: 3px solid black; padding: 10px; font-size: 14px;">
        <b style="font-size: 20px;">Adventure Map Reference</b><br>
        <i style="background-color: purple; width: 20px; height: 10px; display: inline-block;"></i> Day 1 Trails<br>
        <i style="background-color: yellow; width: 20px; height: 10px; display: inline-block;"></i> Day 2 Trails<br>
        <i style="background-color: orange; width: 20px; height: 10px; display: inline-block;"></i> Day 3 Trails<br>
        <i style="background-color: lightgray; width: 12px; height: 12px; display: inline-block; border: 1px solid black;"></i> Bureau of Land Management Rec Site<br>
        <i style="background-color: lightcoral; width: 12px; height: 12px; display: inline-block; border: 1px solid black;"></i> Arches National Park<br>
        <i style="background-color: maroon; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i>Trail Starting and Stopping Points<br>
        <i style="background-color: black; width: 8px; height: 8px; display: inline-block; border-radius: 50%;"></i> Gas Station
        <br><br>
        <idisplay: inline-block;"></i>Application developed by Matthew Cluck using open source technology and data
        from OpenStreetMap, National Park Service, and Bureau of Land Management.<br>
    </div>
'''


description_html = '''
    <div style="background-color: lightgray; border: 3px solid black; padding: 10px; font-size: 14px;">
        <b style="font-size: 20px;">Welcome to your adventure!</b><br>
        <idisplay: inline-block;"></i>Please use this map to guide you on your three day offroad journey around
        Moab, Utah. Use the legend to identify which trails to ride on each day. You can also click the
        trails to see individual names, surface types, and the length of that trail. Use the maroon circles
        as a guide for where to start your ride and where to finish. If you need to gas up, use the black dots
        as a reference to find a gas station. The gray areas of land show the name of the Bureau of Land Management
        Recreation Site when you hover your mouse. Use that to further research interesting sites, rules and regulations of the
        area. Finally, in red shows Arches National Park. That is off limits for offroading. Have fun!<br>
    </div>
'''

# Display all 3 page elements
with col1:
    st.markdown(description_html, unsafe_allow_html=True)

with col2:
    st_folium(m, width='100%')

with col3:
    st.markdown(legend_html, unsafe_allow_html=True)