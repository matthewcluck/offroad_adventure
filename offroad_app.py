import streamlit as st
import folium
from streamlit_folium import st_folium

st.title('Moab 3 Day Offroad Adventure Guide')

# Connect to postgis database
m = folium.Map(location=[38.60, -109.55], zoom_start=11, control_scale=True)

st_folium(m, 1000)
