import streamlit as st
from database import get_livres, emprunter_livre
from notifications import (
    envoyer_mail_emprunt_proprietaire,
    envoyer_mail_emprunt_emprunteur,
)

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
    # Map id -> livre
    livres_par_id = {l["id"]: l for l in livres_dispos}

    options = [f"{l['id']} - {l['titre']} (par {l['auteur']})" for l in livres_dispos]
    selection = st.selectbox("Choisir un livre", options=options)

    emprunteur = st.text_input("Ton nom")
    emprunteur_email = st.text_input("Ton email (ex : prenom.nom@edu-devinci.fr)")
    commentaire = st.text_area("Commentaire (optionnel)")

    if st.button("Emprunter ce livre"):
        if not emprunteur or not emprunteur_email:
            st.error("Merci d’indiquer ton nom et ton email.")
        else:
            id_livre = int(selection.split(" - ")[0])
            livre = livres_par_id[id_livre]

            # 1) Mise à jour base
            date_emprunt, date_retour_prevue = emprunter_livre(
                id_livre,
                emprunteur,
                emprunteur_email,
                commentaire,
            )

            st.success("Le livre a bien été emprunté. Tu as un mois pour le rendre.")

            # 2) Emails
            titre = livre.get("titre") or "Titre inconnu"
            proprietaire = livre.get("proprietaire") or "un membre du club"
            proprietaire_email = livre.get("proprietaire_email") or ""

            # Mail au propriétaire
            try:
                envoyer_mail_emprunt_proprietaire(
                    proprietaire=proprietaire,
                    proprietaire_email=proprietaire_email,
                    emprunteur=emprunteur,
                    emprunteur_email=emprunteur_email,
                    titre=titre,
                    date_emprunt=date_emprunt,
                    date_retour_prevue=date_retour_prevue,
                )
            except Exception as e:
                st.warning(f"L'emprunt est enregistré, mais l'email au propriétaire n'a pas pu être envoyé : {e}")

            # Mail à l'emprunteur
            try:
                envoyer_mail_emprunt_emprunteur(
                    proprietaire=proprietaire,
                    proprietaire_email=proprietaire_email,
                    emprunteur=emprunteur,
                    emprunteur_email=emprunteur_email,
                    titre=titre,
                    date_emprunt=date_emprunt,
                    date_retour_prevue=date_retour_prevue,
                )
            except Exception as e:
                st.warning(f"L'emprunt est enregistré, mais l'email de confirmation n'a pas pu être envoyé : {e}")
