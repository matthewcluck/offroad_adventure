import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv
import psycopg2

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

# Connect to postgis database
load_dotenv()
DATABASE_URL = os.getenv("DB_URL")

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

conn = get_db_connection()

@st.cache_data
def load_geodata():
    sql_queries = {
        "moab_offroad_trails": "SELECT * FROM moab_offroad_trails",
        "national_parks": "SELECT * FROM national_parks WHERE unit_name = 'Arches National Park'",
        "moab_fuel_stations": "SELECT * FROM moab_fuel_stations",
        "blm_ut_rec_sites": "SELECT * FROM blm_ut_rec_sites WHERE \"FET_NAME\" IN ('Canyon Rims','South Moab','Colorado Riverway', 'Labyrinth Rims / Gemini Bridges')",
        "starts_ends": "SELECT * FROM starts_ends"
    }

    moab_offroad_trails_gdf = gpd.read_postgis(sql_queries["moab_offroad_trails"], con=conn, geom_col='combined_geometry')
    national_parks_gdf = gpd.read_postgis(sql_queries["national_parks"], con=conn, geom_col='geometry')
    moab_fuel_stations_gdf = gpd.read_postgis(sql_queries["moab_fuel_stations"], con=conn, geom_col='geometry')
    blm_gdf = gpd.read_postgis(sql_queries["blm_ut_rec_sites"], con=conn, geom_col='geometry')
    starts_ends_gdf = gpd.read_postgis(sql_queries["starts_ends"], con=conn, geom_col='geom')

    return moab_offroad_trails_gdf, national_parks_gdf, moab_fuel_stations_gdf, blm_gdf, starts_ends_gdf

moab_offroad_trails_gdf, national_parks_gdf, moab_fuel_stations_gdf, blm_gdf, starts_ends_gdf = load_geodata()

# Filter trails by day
day_1_trail_names = ["Slickrock", "Slickrock Cutoff", "Slickrock Alternate", "Staircase", "Hell's Revenge 4x4 Trail"]
day_1_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_1_trail_names)]

day_2_trail_names = ["Poison Spider", "Golden Spike", "Portal Trail"]
day_2_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_2_trail_names)]

day_3_trail_names = ["Little Canyon", "Great Escape", "Arth's Corner", "Bull Canyon Road", "Rusty Nail", "Gold Bar Rim"]
day_3_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_3_trail_names)]

m = folium.Map(location=[38.60, -109.58], zoom_start=12, control_scale=True)

# Adding various layers to the map
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

folium.GeoJson(
    starts_ends_gdf,
    name="Adventure Starting and End Points",
    popup=folium.GeoJsonPopup(fields=["Info"]),
    style_function=lambda feature: {
        "fillColor": "black",
        "color": "black",
        "weight": 6
    }
).add_to(m)

folium.LayerControl().add_to(m)

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
        <i style="background-color: black; width: 8px; height: 8px; display: inline-block; border-radius: 50%;"></i> Gas Station
        <br><br>
        <idisplay: inline-block;"></i>Application developed by Matthew Cluck using open source data
        from OpenStreetMap, National Park Service, and Bureau of Land Management.<br>
    </div>
'''


description_html = '''
    <div style="background-color: lightgray; border: 3px solid black; padding: 10px; font-size: 14px;">
        <b style="font-size: 20px;">Welcome to your adventure!</b><br>
        <idisplay: inline-block;"></i>Please use this map to guide you on your three day offroad journey around
        Moab, Utah. Use the legend to identify which trails to ride on each day. You can also click the
        trails to see individual names, surface types, and the length of that trail. Use the blue waypoints
        as a guide for where to start your ride and where to finish. If you need to gas up, use the black dots
        as a reference to find a gas station. The gray areas of land show the name of the Bureau of Land Management
        Recreation Site when you hover your mouse. Use that to further research interesting sites, rules and regulations of the
        area. Finally, in red shows Arches National Park. That is off limits for offroading. Have fun!<br>
    </div>
'''

# Display the map in the first column
with col1:
    st.markdown(description_html, unsafe_allow_html=True)

# Display legend in the second column
with col2:
    st_folium(m, width='100%')

with col3:
    st.markdown(legend_html, unsafe_allow_html=True)