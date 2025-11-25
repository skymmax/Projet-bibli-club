import streamlit as st
from database import get_livres, rendre_livre

st.set_page_config(page_title="Rendre un livre",    page_icon="assets/logo_icone.png",)

st.title("Rendre un livre")
st.write("Sélectionne un livre actuellement emprunté pour le marquer comme rendu.")


# --- Récupération des livres ---
livres_rows = get_livres()
livres = [dict(row) for row in livres_rows]

# On ne liste que les livres indisponibles
livres_empruntes = [l for l in livres if l["disponibilite"] == "Indisponible"]

if not livres_empruntes:
    st.info("Aucun livre n'est actuellement enregistré comme emprunté.")
else:
    livre_selection = st.selectbox(
        "Livre à rendre",
        options=[f"{l['id']} - {l['titre']} (emprunté par {l['emprunte_par']})" for l in livres_empruntes]
    )

    commentaire = st.text_area("Commentaire (optionnel, état du livre, remarques, etc.)")

    if st.button("Marquer comme rendu"):
        id_livre = int(livre_selection.split(" - ")[0])
        rendre_livre(id_livre, commentaire)
        st.success("Le livre a bien été marqué comme rendu !")
