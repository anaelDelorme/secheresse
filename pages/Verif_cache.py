import streamlit as st

def show_cache_info():
    # Afficher les informations du cache
    cache_info = st.cache_info()
    st.write("Cache Info:", cache_info)

# Créez une page pour afficher les informations du cache
if st.sidebar.button("Vérifier le Cache"):
    show_cache_info()