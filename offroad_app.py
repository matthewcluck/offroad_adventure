import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv
import psycopg2

st.title('Moab 3 Day Offroad Adventure Guide aa')

# Connect to postgis database
load_dotenv()
DATABASE_URL = os.getenv("DB_URL")

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# Establish connection
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

    # Read data from PostgreSQL
    moab_offroad_trails_gdf = gpd.read_postgis(sql_queries["moab_offroad_trails"], con=conn, geom_col='combined_geometry')
    national_parks_gdf = gpd.read_postgis(sql_queries["national_parks"], con=conn, geom_col='geometry')
    moab_fuel_stations_gdf = gpd.read_postgis(sql_queries["moab_fuel_stations"], con=conn, geom_col='geometry')
    blm_gdf = gpd.read_postgis(sql_queries["blm_ut_rec_sites"], con=conn, geom_col='geometry')
    starts_ends_gdf = gpd.read_postgis(sql_queries["starts_ends"], con=conn, geom_col='geom')

    return moab_offroad_trails_gdf, national_parks_gdf, moab_fuel_stations_gdf, blm_gdf, starts_ends_gdf

# Load the data
moab_offroad_trails_gdf, national_parks_gdf, moab_fuel_stations_gdf, blm_gdf, starts_ends_gdf = load_geodata()

# Filter trails by day
day_1_trail_names = ["Slickrock", "Slickrock Cutoff", "Slickrock Alternate", "Staircase", "Hell's Revenge 4x4 Trail"]
day_1_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_1_trail_names)]

day_2_trail_names = ["Poison Spider", "Golden Spike", "Portal Trail"]
day_2_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_2_trail_names)]

day_3_trail_names = ["Little Canyon", "Great Escape", "Arth's Corner", "Bull Canyon Road", "Rusty Nail", "Gold Bar Rim"]
day_3_trails = moab_offroad_trails_gdf[moab_offroad_trails_gdf["name"].isin(day_3_trail_names)]

m = folium.Map(location=[38.60, -109.55], zoom_start=11, control_scale=True)

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

folium.GeoJson(
    national_parks_gdf,
    name="National Parks",
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

st_folium(m, 1000)
