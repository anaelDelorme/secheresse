import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import warnings
import folium
import requests
import fonctionsSecheresse

from streamlit_folium import folium_static



warnings.filterwarnings('ignore', 'GeoSeries.notna', UserWarning)

st.set_page_config(page_title="Carte des arrêtés de sécheresse - eaux souterraines", page_icon="💦")

st.markdown("# Eaux souterraines")
st.sidebar.header("Eaux souterraines")
st.markdown(
    """Cette carte présente l'ensemble des arrêtés de sécheresse à la date de jour sur les eaux souterraines.    
    Les arrêtés de sécheresse ont 4 niveaux d'alerte :      
   <span style='background-color:#FAED93; display:inline-block; width:20px; height:20px;'></span> Vigilance      
   <span style='background-color:#FAC939; display:inline-block; width:20px; height:20px;'></span> Alerte      
   <span style='background-color:#FA78C5; display:inline-block; width:20px; height:20px;'></span> Alerte renforcée      
   <span style='background-color:#FA2048; display:inline-block; width:20px; height:20px;'></span> Crise     
    """,
    unsafe_allow_html=True
)
with st.spinner('Chargement en cours...'):
    carte = fonctionsSecheresse.create_carte_jour(type = "SOU")
    st.markdown(carte._repr_html_(), unsafe_allow_html=True)
        
