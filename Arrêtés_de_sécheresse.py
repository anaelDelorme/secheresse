import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Sécheresse en France : les arrêtés! 👋")

st.sidebar.success("Choisis une carte ou l'analyse historique.")

st.markdown(
    """
    Ce site présente les mesures de suspension ou de limitation prises par les préfets à partir des données fournies à titre indicatif par les services départementaux de l'état.
    **👈 Choisis une carte ou l'analyse statistique**
    ### En savoir plus :
    - Données Sécheresse sur data.gouv.fr [Données sur data gouv](https://www.data.gouv.fr/fr/datasets/donnee-secheresse-propluvia/)
    - Site Propluvia [Propluvia](http://propluvia.developpement-durable.gouv.fr/propluvia/faces/index.jsp)
    ### Détail des niveaux d'alerte :
    <span style='background-color:#FAED93; display:inline-block; width:20px; height:20px;'></span> Vigilance : Information et incitation des particuliers et des professionnels à faire des économies d'eau      
    <span style='background-color:#FAC939; display:inline-block; width:20px; height:20px;'></span> Alerte : Réduction des prélèvements à des fins agricoles inférieure à 50% (ou interdiction jusqu'à 3 jours par semaine), mesures d'interdiction de manœuvre de vanne, d'activité nautique, interdiction à certaines heures d'arroser les jardins, espaces verts, golfs, de laver sa voiture, ...     
    <span style='background-color:#FA78C5; display:inline-block; width:20px; height:20px;'></span> Alerte renforcée : Réduction des prélèvements à des fins agricoles supérieure ou égale à 50% (ou interdiction supérieure ou égale à 3,5 jours par semaine), limitation plus forte des prélèvements pour l'arrosage des jardins, espaces verts, golfs, lavage des voitures, ..., jusqu'à l'interdiction de certains prélèvements          
    <span style='background-color:#FA2048; display:inline-block; width:20px; height:20px;'></span> Crise : Arrêt des prélèvements non prioritaires y compris des prélèvements à des fins agricoles. Seuls les prélèvements permettant d'assurer l'exercice des usages prioritaires sont autorisés (santé, sécurité civile, eau potable, salubrité)       
"""
)