
import streamlit as st
import folium
from streamlit.components.v1 import html
from kelompok_vds import create_map

st.set_page_config(page_title="Dashboard Penyakit Jakarta", layout="wide")

st.title("🗺️ Dashboard Persebaran Penyakit di Jakarta")
selected = st.selectbox("Pilih jenis penyakit", ["COVID-19", "TBC", "ISPA"])

m = create_map(selected)
m.save("map.html")

with open("map.html", "r", encoding="utf-8") as f:
    map_html = f.read()

html(map_html, height=700)
