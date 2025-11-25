import streamlit as st
from database import init_db
from pathlib import Path

# Charger et afficher le logo
logo_path = Path("assets/logo.png")

if logo_path.exists():
    st.image(str(logo_path), width=200)

# Configuration de la page principale
st.set_page_config(
    page_title="Bibliothèque du Club Entrepreneurs",
    page_icon="assets/logo_icone.png",
    layout="wide"
)

# Initialisation de la base de données
init_db()

# Titre principal
st.title("Bibliothèque du Club Entrepreneurs")

# Introduction
st.markdown("""
Bienvenue sur la plateforme de gestion et de partage des livres du Club Entrepreneurs.

Cet outil a été conçu pour permettre aux membres du club de :
- consulter les ouvrages disponibles ;
- ajouter facilement leurs propres livres à la bibliothèque commune ;
- emprunter et rendre des ouvrages en quelques secondes ;
- suivre l’historique des emprunts.

Utilisez le menu situé à gauche pour accéder aux différentes sections de l’application : 
le catalogue, l’ajout de livre, la gestion des emprunts et l’historique.
""")

# Séparateur
st.markdown("---")

# Section complémentaire (optionnelle)
st.markdown("""
### À propos du projet

Cette plateforme a été développée pour encourager le partage de connaissances
et faciliter l’accès à des ressources utiles en entrepreneuriat, management,
développement personnel et domaines associés.  
N’hésitez pas à contribuer en ajoutant vos livres ou en partageant vos retours.
""")
st.markdown("Bonne lecture à tous ! ")