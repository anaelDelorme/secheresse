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
    
    data_geo_simplify = recup_zones_actives()
    arretes = recup_data_arrete_du_jour()
    arretes_publie = arretes[arretes['statut_arrete'] == "Publié"]
    geo_merge = data_geo_simplify.merge(arretes_publie, on = 'id_zone')
    colonnes_selectionnees = ['id_zone',
                                'code_zone',	
                                'type_zone',
                                'nom_zone' ,
                                'geometry', 
                                'numero_niveau',
                                'nom_niveau',
                                'id_arrete',
                                'numero_arrete',
                                'numero_arrete_cadre',
                                'date_signature',	
                                'debut_validite_arrete',	
                                'fin_validite_arrete']

    gdf_selection = geo_merge.loc[:, colonnes_selectionnees]
    gdf_non_vide = gdf_selection[~gdf_selection['geometry'].is_empty & gdf_selection['geometry'].notna()].dropna(subset=['geometry'])
    gdf_sup = gdf_non_vide[gdf_non_vide['type_zone'] == "SUP"]

    latitude = 46.1
    longitude = 2.2
    m = folium.Map(location=[latitude, longitude], zoom_start=5)

    niveaux = ['Vigilance', 'Alerte', 'Alerte renforcée', 'Crise']
    couleurs = ['#FAED93', '#FAC939', '#FA78C5', '#FA2048']
    couleur_map = dict(zip(niveaux, couleurs))

    colonnes_tooltip = colonnes_selectionnees.copy()
    colonnes_tooltip.remove('geometry')


    colonnes_tooltip_alias = []
    for colonne in colonnes_tooltip:
        colonne_alias = colonne.replace("_", " ").capitalize()
        colonnes_tooltip_alias.append(colonne_alias)

    folium.GeoJson(gdf_sup, style_function=style_function, tooltip=folium.features.GeoJsonTooltip(
                fields=colonnes_tooltip,
                aliases=colonnes_tooltip_alias,
                sticky=True,
                opacity=0.9,
                direction='right',
            )).add_to(m)
    folium_static(m)