import streamlit as st
from database import ajouter_livre

st.set_page_config(page_title="Ajouter un livre",)

st.title("Ajouter un livre")
st.write("Remplis les informations ci-dessous pour ajouter un livre à la bibliothèque du club.")

# --- Formulaire ---
with st.form("ajout_livre_form"):

    titre = st.text_input("Titre du livre")
    auteur = st.text_input("Auteur")
    categorie = st.selectbox(
        "Catégorie",
        ["Business", "Mindset", "Finance", "Marketing", "Management", "Développement personnel", "Autre"]
    )
    proprietaire = st.text_input("Propriétaire (ton nom)")
    resume = st.text_area("Résumé (optionnel)")
    couverture = st.text_input("URL de couverture (optionnel)")

    submitted = st.form_submit_button("Ajouter le livre")

    if submitted:
        if not titre or not proprietaire:
            st.error("Le titre et le propriétaire sont obligatoires.")
        else:
            ajouter_livre(titre, auteur, categorie, proprietaire, resume, couverture)
            st.success(f"Le livre **{titre}** a été ajouté avec succès ! 🎉")
