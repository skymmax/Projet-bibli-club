import streamlit as st
from database import get_livres, rendre_livre, get_dernier_emprunt
from notifications import (
    envoyer_mail_retour_proprietaire,
    envoyer_mail_retour_emprunteur,
)

st.set_page_config(page_title="Rendre un livre",    page_icon="assets/logo_icone.png",)



st.title("Rendre un livre")
st.write("Sélectionne un livre actuellement emprunté pour le marquer comme rendu.")

livres_rows = get_livres()
livres = [dict(row) for row in livres_rows]

livres_empruntes = [l for l in livres if l["disponibilite"] == "Indisponible"]

if not livres_empruntes:
    st.info("Aucun livre n'est actuellement enregistré comme emprunté.")
else:
    livres_par_id = {l["id"]: l for l in livres_empruntes}

    selection = st.selectbox(
        "Livre à rendre",
        options=[f"{l['id']} - {l['titre']} (emprunté par {l['emprunte_par']})" for l in livres_empruntes]
    )

    commentaire = st.text_area("Commentaire (optionnel, état du livre, remarques, etc.)")

    if st.button("Marquer comme rendu"):
        id_livre = int(selection.split(" - ")[0])

        # 1) Mise à jour DB
        rendre_livre(id_livre, commentaire)
        st.success("Le livre a bien été marqué comme rendu.")

        # 2) Récupérer le dernier emprunt pour les emails
        info = get_dernier_emprunt(id_livre)
        if info is None:
            st.warning("Impossible de retrouver les informations de l'emprunt pour envoyer les emails.")
        else:
            titre = info.get("titre") or "Titre inconnu"
            proprietaire = info.get("proprietaire") or "le propriétaire"
            proprietaire_email = info.get("proprietaire_email") or ""
            emprunteur = info.get("emprunteur") or "l'emprunteur"
            emprunteur_email = info.get("emprunteur_email") or ""
            date_emprunt = info.get("date_emprunt") or ""
            date_retour_prevue = info.get("date_retour_prevue") or ""
            date_retour = info.get("date_retour")  # normalement renseignée par rendre_livre

            # Mail au propriétaire
            try:
                envoyer_mail_retour_proprietaire(
                    proprietaire=proprietaire,
                    proprietaire_email=proprietaire_email,
                    emprunteur=emprunteur,
                    emprunteur_email=emprunteur_email,
                    titre=titre,
                    date_emprunt=date_emprunt,
                    date_retour_prevue=date_retour_prevue,
                    date_retour=date_retour,
                )
            except Exception as e:
                st.warning(f"Le retour est enregistré, mais l'email au propriétaire n'a pas pu être envoyé : {e}")

            # Mail à l'emprunteur
            try:
                envoyer_mail_retour_emprunteur(
                    proprietaire=proprietaire,
                    proprietaire_email=proprietaire_email,
                    emprunteur=emprunteur,
                    emprunteur_email=emprunteur_email,
                    titre=titre,
                    date_emprunt=date_emprunt,
                    date_retour_prevue=date_retour_prevue,
                    date_retour=date_retour,
                )
            except Exception as e:
                st.warning(f"Le retour est enregistré, mais l'email de confirmation n'a pas pu être envoyé : {e}")
