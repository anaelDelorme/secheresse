import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import warnings
import folium
import requests
import branca
from streamlit_folium import folium_static





warnings.filterwarnings('ignore', 'GeoSeries.notna', UserWarning)

st.set_page_config(page_title="Carte annuelle de la durée totale des arrêtés de sécheresse", page_icon="💦")

st.markdown("# Carte annuelle des arrêtés")
st.sidebar.header("Carte annuelle des arrêtés")
st.markdown(
    """Cette carte présente la durée cumulée des arrêtés de sécheresse par zone et par année.    
    Tous les niveaux d'alerte sont agrégés.   
    """,
    unsafe_allow_html=True
)

@st.cache_data
def recup_data_arrete(url):
        response = requests.get(url)
        if response.status_code != 200:
            return("pas de connexion")
        else:
            data = pd.read_csv(url)
            return(data)
        
urls = {
    '2010' : "https://www.data.gouv.fr/fr/datasets/r/d6cb1826-6cc8-4709-85fd-433db23aa951",    
    '2011' : "https://www.data.gouv.fr/fr/datasets/r/227149be-cd8b-4e59-a1a9-0840ef7f0a24",
    '2012' : "https://www.data.gouv.fr/fr/datasets/r/43864992-e79b-449e-9d7d-93dad9b9df59",
    '2013' : "https://www.data.gouv.fr/fr/datasets/r/f9c1da33-19f4-499d-88cc-b3c247484215",
    '2014' : "https://www.data.gouv.fr/fr/datasets/r/c68362d9-93ff-46bc-99a6-35d506855dae",    
    '2015' : "https://www.data.gouv.fr/fr/datasets/r/98cb1f80-f296-4eae-a0b3-f236fc0b9325",
    '2016' : "https://www.data.gouv.fr/fr/datasets/r/fbd87d0b-a504-49e2-be6e-66a96ca4e489",
    '2017' : "https://www.data.gouv.fr/fr/datasets/r/ab886886-9b64-47ca-8604-49c9910c0b74",
    '2018' : "https://www.data.gouv.fr/fr/datasets/r/8ba1889e-5496-47a6-8bf3-9371086dd65c",
    '2019' : "https://www.data.gouv.fr/fr/datasets/r/ed2e6cfa-1fe7-40a6-95bb-d9e6f99a78a0",
    '2020' : "https://www.data.gouv.fr/fr/datasets/r/d16ae5b1-6666-4caa-930c-7993c4cd4188",
    '2021' : "https://www.data.gouv.fr/fr/datasets/r/c23fe783-763f-4669-a9b7-9d1d199fcfcd",
    '2022' : "https://www.data.gouv.fr/fr/datasets/r/0fee8de1-c6de-4334-8daf-654549e53988",
    '2023' : "https://www.data.gouv.fr/fr/datasets/r/782aac32-29c8-4b66-b231-ab4c3005f574"
}

with st.spinner('Chargement en cours...'):
    for key, value in urls.items():
        # Création du nom de l'objet en concaténant "data_" avec la clé
        nom_objet = "data_" + key

        # Création de l'objet avec le nom spécifié
        globals()[nom_objet] = recup_data_arrete(value)
        
    def maj_dataframe(data_frame):
        data_frame['debut_validite_arrete'] = pd.to_datetime(data_frame['debut_validite_arrete'])
        data_frame['fin_validite_arrete'] = pd.to_datetime(data_frame['fin_validite_arrete'])
        data_frame['duree_validite_arrete'] = (data_frame['fin_validite_arrete'] - data_frame['debut_validite_arrete']).dt.days
        data_frame['annee'] = data_frame['debut_validite_arrete'].dt.year
        data_frame = data_frame[['id_arrete', 'id_zone', 'annee', 'numero_niveau', 'nom_niveau', 'duree_validite_arrete']]
        return(data_frame)

    dataframes_maj = []
    for annee in urls.keys():
        # Récupération du DataFrame correspondant à l'année
        df = globals().get(f'data_{annee}')
        
        # Vérification si le DataFrame existe
        if df is not None:
            # Application de la fonction maj_dataframe(df)
            df_maj = maj_dataframe(df)
                
            # Ajout du DataFrame mis à jour à la liste
            dataframes_maj.append(df_maj)

    # Concaténation de tous les DataFrames avec le suffixe "_maj"
    data_tous_arretes = pd.concat(dataframes_maj, axis=0)
    
    data_agrege = data_tous_arretes[data_tous_arretes['nom_niveau']!="Absence de restriction"].groupby(['annee','id_zone']).agg(
        total_duree = ('duree_validite_arrete', 'sum'),
        nombre_observations=('nom_niveau', 'size')
    )

    data_agrege = data_agrege.reset_index(level = ['annee','id_zone'])
    data_agrege_annee = data_agrege[str(data_agrege['annee']) == "2010"]
    
    @st.cache_data
    def recup_toutes_zones():
        zones = gpd.read_file("data/all_zones_simplify.json")
        return(zones)
    data_geo_simplify = recup_toutes_zones()

    geo_merge = data_geo_simplify.merge(data_agrege, on = 'id_zone')
                                       
    colonnes_selectionnees = ['id_zone','geometry', 'code_zone','nom_zone','total_duree']
    gdf_selection = geo_merge.loc[:, colonnes_selectionnees]
    
    latitude = 46.1
    longitude = 2.2
    m = folium.Map(location=[latitude, longitude], zoom_start=5, tiles="cartodb positron", )

    colonnes_tooltip = colonnes_selectionnees.copy()
    colonnes_tooltip.remove('geometry')

    colonnes_tooltip_alias = []
    for colonne in colonnes_tooltip:
            colonne_alias = colonne.replace("_", " ").capitalize()
            colonnes_tooltip_alias.append(colonne_alias)
            
    min_value = gdf_selection['total_duree'].min()
    max_value = gdf_selection['total_duree'].max()
    num_elements = 6

    liste_chiffres = np.linspace(min_value, max_value, num_elements)
    liste_arrondie = np.round(liste_chiffres, -1).astype(int)

    colormap  = branca.colormap.linear.YlOrRd_09.scale(min_value, max_value )
    colormap = colormap.to_step(index=liste_arrondie)
    colormap.caption = 'Durée sous arrêtés par zone (en nombre de jours cumulés)'
    colormap.add_to(m)

    def style_function(feature):
                nb = feature["properties"]["total_duree"]
                return {
                    "fillOpacity": 0.7,
                    "weight": 0,
                    "fillColor": '#gray' if nb is None else colorscale(nb),
                    "color": "#D9D9D9"
                }    

    folium.GeoJson(gdf_selection, style_function=style_function, tooltip=folium.features.GeoJsonTooltip(
                    fields=colonnes_tooltip,
                    aliases=colonnes_tooltip_alias,
                    sticky=True,
                    opacity=0.9,
                    direction='right',
                )).add_to(m)

    folium_static(m)

    
    
    