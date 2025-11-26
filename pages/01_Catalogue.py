import streamlit as st
from database import get_livres

st.set_page_config(page_title="Catalogue de la bibliothèque", page_icon="assets/logo_icone.png",
)

st.title("Catalogue de la bibliothèque du Club")
st.write("Retrouve ici tous les livres partagés par les membres du club.")


# --- Chargement des livres ---
livres_rows = get_livres()

if not livres_rows:
    st.info("Aucun livre pour le moment. Ajoute ton premier livre dans l'onglet ** Ajouter un livre**.")
else:
    # Conversion des lignes SQLite en dictionnaires
    livres = [dict(row) for row in livres_rows]
    # On enlève les livres archivés du catalogue public
    livres = [l for l in livres if l.get("disponibilite") != "Archivé"]


    # --- Barre latérale de filtres ---
    st.sidebar.header("Filtres")

    # Récupération des valeurs uniques
    categories = sorted({livre["categorie"] for livre in livres if livre["categorie"]})
    proprietaires = sorted({livre["proprietaire"] for livre in livres if livre["proprietaire"]})
    disponibilites = sorted({livre["disponibilite"] for livre in livres if livre["disponibilite"]})

    # Filtres avec option "Tous"
    categorie_filtre = st.sidebar.selectbox(
        "Catégorie",
        options=["Toutes"] + categories if categories else ["Toutes"]
    )

    dispo_filtre = st.sidebar.selectbox(
        "Disponibilité",
        options=["Toutes"] + disponibilites if disponibilites else ["Toutes"]
    )

    proprio_filtre = st.sidebar.selectbox(
        "Propriétaire",
        options=["Tous"] + proprietaires if proprietaires else ["Tous"]
    )

    recherche = st.sidebar.text_input("Recherche (titre ou auteur)")

    # --- Application des filtres ---
    livres_filtres = livres

    if categorie_filtre != "Toutes":
        livres_filtres = [l for l in livres_filtres if l.get("categorie") == categorie_filtre]

    if dispo_filtre != "Toutes":
        livres_filtres = [l for l in livres_filtres if l.get("disponibilite") == dispo_filtre]

    if proprio_filtre != "Tous":
        livres_filtres = [l for l in livres_filtres if l.get("proprietaire") == proprio_filtre]

    if recherche:
        recherche_lower = recherche.lower()
        livres_filtres = [
            l for l in livres_filtres
            if recherche_lower in (l.get("titre") or "").lower()
            or recherche_lower in (l.get("auteur") or "").lower()
        ]

    st.subheader(f"Livres trouvés : {len(livres_filtres)}")

    if not livres_filtres:
        st.warning("Aucun livre ne correspond à ces filtres.")
    else:
        # Affichage sous forme de tableau simple
        colonnes_affichees = ["titre", "auteur", "categorie", "proprietaire", "disponibilite", "emprunte_par"]
        en_tetes = {
            "titre": "Titre",
            "auteur": "Auteur",
            "categorie": "Catégorie",
            "proprietaire": "Propriétaire",
            "disponibilite": "Disponibilité",
            "emprunte_par": "Emprunté par"
        }

        # On transforme en liste de dicts filtrés avec clés propres
        data_affichee = []
        for l in livres_filtres:
            row = {en_tetes[col]: l.get(col) for col in colonnes_affichees}
            data_affichee.append(row)

        st.dataframe(data_affichee, use_container_width=True)

# -- IGNORE ---