import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts
import requests
from streamlit_echarts import st_pyecharts



st.set_page_config(page_title="Analyse historique des arrêtés de sécheresse", page_icon="💦", layout="wide")

st.markdown("# Analyse historique des arrêtés de sécheresse")
st.sidebar.header(" Analyse historique")
st.markdown(
    """### Nombre de jours annuels concernés par des arrêtés de sécheresse
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
        data_frame['debut_validite_arrete'] = pd.to_datetime(data_frame['debut_validite_arrete'], errors='coerce')
        data_frame['fin_validite_arrete'] = pd.to_datetime(data_frame['fin_validite_arrete'], errors='coerce')
        data_frame = data_frame.dropna(subset=['debut_validite_arrete', 'fin_validite_arrete'])
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
    data_tous_arretes = data_tous_arretes.drop_duplicates()


    data_agrege = data_tous_arretes[data_tous_arretes['nom_niveau']!="Absence de restriction"].groupby(['annee','nom_niveau']).agg(
            total_duree = ('duree_validite_arrete', 'sum'),
            nombre_observations=('nom_niveau', 'size')
        )

    data_agrege = data_agrege.reset_index(level = ['annee','nom_niveau'])

    data_pivot = data_agrege.pivot(index='annee', columns='nom_niveau', values='total_duree').reset_index()

def format_with_space(params):
    value = params.value
    return "{:,.0f}".format(value).replace(",", " ")

b = (
    Bar(
        opts.InitOpts(
            #theme = ThemeType.DARK,
            width = "1024px",
            height = "600px"
        )
    )
    .add_xaxis(data_pivot.annee.tolist())
    .add_yaxis(
        "Vigilance",
        data_pivot["Vigilance"].tolist(),
        stack= "Ad",
        color="#FAED93",
    ).add_yaxis(
        "Alerte",
        data_pivot["Alerte"].tolist(),
        stack= "Ad",
        color="#FAC939",
    ).add_yaxis(
        "Alerte renforcée",
        data_pivot["Alerte renforcée"].tolist(),
        stack= "Ad",
        color="#FA78C5",
    ).add_yaxis(
        "Arrêt des prélèvements non prioritaires",
        data_pivot["Arrêt des prélèvements non prioritaires"].tolist(),
        stack= "Ad",
        color="#FA9778",
    ).add_yaxis(
        "Crise modérée",
        data_pivot["Crise modérée"].tolist(),
        stack= "Ad",
        color="#FB6C86",
    ).add_yaxis(
        "Crise",
        data_pivot["Crise"].tolist(),
        stack= "Ad",
        color="#FA2048",
    ).add_yaxis(
        "Crise renforcée",
        data_pivot["Crise renforcée"].tolist(),
        stack= "Ad",
        color="#7A1023",
    ).set_series_opts(label_opts=opts.LabelOpts(is_show=False)
    ).set_global_opts(
        # Configure other options for the chart (e.g., title, axis labels)
        xaxis_opts=opts.AxisOpts(name="Année"),
        yaxis_opts=opts.AxisOpts(name="Durée totale en nombre de jours",
                                 axislabel_opts={"formatter": format_with_space}
                                 )  # Ajouter un espace comme délimiteur des milliers

    )
)

st_pyecharts(b, height=600)


