import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

st.set_page_config(page_title="Carte des arrêtés de sécheresse - eaux superficielles", page_icon="📈")

st.markdown("# Eaux superficielles")
st.sidebar.header("Eaux superficielles")
st.write(
    """Cette carte présente l'ensemble des arrêtés de sécheresse à la date de jour sur les eaux superficielles. Les arrêtés de sécheresse ont 4 niveaux d'alerte représentés par 4 niveaux de couleur sur la carte."""
)

data_geo_simplify = gpd.read_file("data/active_zones_simplify.json")
arretes = pd.read_csv("data/arretes.csv")
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
gdf_selection = gdf_selection[~gdf['geometry'].is_empty & gdf['geometry'].notna()]

colors = {'Vigilance': '#FAED93', 'Alerte': '#FAC939', 'Alerte renforcée': '#FA78C5', 'Crise': '#FA2048'}
cmap = ListedColormap([colors[level] for level in sorted(colors.keys())])

st.write(gdf_selection[gdf_selection['type_zone']=="SUP"].explore(column='nom_niveau', cmap = cmap, tooltip=True))