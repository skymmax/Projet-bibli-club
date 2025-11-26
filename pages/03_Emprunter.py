import streamlit as st
from database import get_livres, emprunter_livre

st.set_page_config(page_title="Emprunter un livre",    page_icon="assets/logo_icone.png",
)

st.title("Emprunter un livre")
st.write("Sélectionne un livre disponible ci-dessous pour l’emprunter.")

livres_rows = get_livres()
livres = [dict(row) for row in livres_rows]

livres_dispos = [l for l in livres if l["disponibilite"] == "Disponible"]

if not livres_dispos:
    st.info("Aucun livre disponible pour le moment.")
else:
    livre_selection = st.selectbox(
        "Choisir un livre",
        options=[f"{l['id']} - {l['titre']} (par {l['auteur']})" for l in livres_dispos]
    )

    emprunteur = st.text_input("Ton nom")
    emprunteur_email = st.text_input("Ton email DeVinci")
    commentaire = st.text_area("Commentaire (optionnel)")

    if st.button("Emprunter ce livre"):
        if not emprunteur or not emprunteur_email:
            st.error("Merci d’indiquer ton nom et ton email.")
        else:
            id_livre = int(livre_selection.split(" - ")[0])
            emprunter_livre(id_livre, emprunteur, emprunteur_email, commentaire)
            st.success("Le livre a bien été emprunté. Tu as un mois pour le rendre.")