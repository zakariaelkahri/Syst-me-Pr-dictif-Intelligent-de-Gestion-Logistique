import streamlit as st
import pandas as pd
import numpy as np
import os
from pymongo import MongoClient

# Page configuration
st.set_page_config(
    page_title="Système Prédictif Intelligent de Gestion Logistique",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Système Prédictif Intelligent de Gestion Logistique")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choisir une page", ["Accueil", "Données", "Analytics"])

# MongoDB connection
@st.cache_resource
def init_mongo_connection():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    try:
        client = MongoClient(mongo_uri)
        return client
    except Exception as e:
        st.error(f"Erreur de connexion à MongoDB: {e}")
        return None

if page == "Accueil":
    st.header("🏠 Accueil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 État du Système")
        
        # MongoDB Status
        mongo_client = init_mongo_connection()
        if mongo_client:
            st.success("✅ MongoDB connecté")
            try:
                # Test connection
                mongo_client.admin.command('ping')
                st.success("✅ MongoDB opérationnel")
            except Exception as e:
                st.error(f"❌ Erreur MongoDB: {e}")
        else:
            st.error("❌ MongoDB déconnecté")
        
        # Airflow Status
        airflow_url = os.getenv("AIRFLOW_URL", "http://localhost:8080")
        st.info(f"🔗 Airflow: {airflow_url}")
    
    with col2:
        st.subheader("📊 Aperçu des Données")
        
        # Check if data file exists
        data_path = "data/dataset/DataCoSupplyChainDataset.csv"
        if os.path.exists(data_path):
            try:
                df = pd.read_csv(data_path, nrows=100)  # Load first 100 rows for preview
                st.success(f"✅ Dataset chargé: {len(df)} échantillons")
                st.write(f"Colonnes: {len(df.columns)}")
                
                with st.expander("Voir un aperçu des données"):
                    st.dataframe(df.head())
                    
            except Exception as e:
                st.error(f"Erreur lors du chargement: {e}")
        else:
            st.warning("⚠️ Dataset non trouvé")

elif page == "Données":
    st.header("📊 Gestion des Données")
    
    # Data loading section
    st.subheader("Chargement des Données")
    
    data_path = "data/dataset/DataCoSupplyChainDataset.csv"
    if os.path.exists(data_path):
        try:
            df = pd.read_csv(data_path)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nombre de lignes", len(df))
            with col2:
                st.metric("Nombre de colonnes", len(df.columns))
            with col3:
                st.metric("Taille (MB)", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}")
            
            # Data preview
            st.subheader("Aperçu des Données")
            st.dataframe(df.head(50))
            
            # Data info
            with st.expander("Informations sur les Colonnes"):
                st.write(df.dtypes)
                
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
    else:
        st.error("Dataset non trouvé!")

elif page == "Analytics":
    st.header("📈 Analytics et Visualisations")
    st.info("Tableau de bord pour l'analyse des données logistiques.")
    
    # Placeholder for analytics
    if os.path.exists("data/dataset/DataCoSupplyChainDataset.csv"):
        try:
            df = pd.read_csv("data/dataset/DataCoSupplyChainDataset.csv", nrows=500)
            
            st.subheader("Statistiques Rapides")
            
            # Simple metrics
            if len(df) > 0:
                st.write(f"**Total des enregistrements:** {len(df)}")
                
                # Show numeric columns if available
                numeric_columns = df.select_dtypes(include=[np.number]).columns
                if len(numeric_columns) > 0:
                    selected_column = st.selectbox("Choisir une colonne numérique", numeric_columns)
                    if selected_column:
                        st.bar_chart(df[selected_column].value_counts().head(10))
                        
        except Exception as e:
            st.error(f"Erreur: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Système Prédictif Intelligent**")
st.sidebar.markdown("Version 1.0")
st.sidebar.markdown("🚀 Powered by Streamlit")