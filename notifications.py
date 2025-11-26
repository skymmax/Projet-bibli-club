# notifications.py
"""
Toutes les définitions d'emails : textes + envoi via email_utils.
On centralise ici pour pouvoir modifier facilement les messages.
"""

from email_utils import envoyer_email


# --- Emprunt ---

def envoyer_mail_emprunt_proprietaire(
    proprietaire: str,
    proprietaire_email: str,
    emprunteur: str,
    emprunteur_email: str,
    titre: str,
    date_emprunt: str,
    date_retour_prevue: str,
):
    """
    Email envoyé au propriétaire quand quelqu'un emprunte son livre.
    """
    if not proprietaire_email:
        return  # rien à faire si on n'a pas l'email

    sujet = f"Votre livre « {titre} » a été emprunté"

    contenu = (
        f"Bonjour {proprietaire},\n\n"
        f"Votre livre « {titre} » a été emprunté via la bibliothèque du Club Entrepreneurs.\n\n"
        f"Emprunteur : {emprunteur}\n"
        f"Adresse email de l'emprunteur : {emprunteur_email}\n\n"
        f"Date d'emprunt : {date_emprunt}\n"
        f"Date de retour prévue : {date_retour_prevue}\n\n"
        f"Si besoin, vous pouvez contacter directement l'emprunteur à cette adresse : {emprunteur_email}.\n\n"
        f"Ceci est un message automatique envoyé par la bibliothèque du club."
    )

    envoyer_email(proprietaire_email, sujet, contenu)


def envoyer_mail_emprunt_emprunteur(
    proprietaire: str,
    proprietaire_email: str,
    emprunteur: str,
    emprunteur_email: str,
    titre: str,
    date_emprunt: str,
    date_retour_prevue: str,
):
    """
    Email envoyé à l'emprunteur pour confirmer l'emprunt et lui donner les infos utiles.
    """
    if not emprunteur_email:
        return

    sujet = f"Confirmation de l'emprunt de « {titre} »"

    contenu = (
        f"Bonjour {emprunteur},\n\n"
        f"Vous avez emprunté le livre « {titre} » via la bibliothèque du Club Entrepreneurs.\n\n"
        f"Propriétaire : {proprietaire}\n"
        f"Adresse email du propriétaire : {proprietaire_email}\n\n"
        f"Date d'emprunt : {date_emprunt}\n"
        f"Date de retour prévue : {date_retour_prevue}\n\n"
        f"Merci de respecter un délai maximum d'un mois pour le retour du livre.\n"
        f"En cas de problème ou de retard, pensez à prévenir le propriétaire et le club.\n\n"
        f"Ceci est un message automatique envoyé par la bibliothèque du club."
    )

    envoyer_email(emprunteur_email, sujet, contenu)


# --- Retour ---

def envoyer_mail_retour_proprietaire(
    proprietaire: str,
    proprietaire_email: str,
    emprunteur: str,
    emprunteur_email: str,
    titre: str,
    date_emprunt: str,
    date_retour_prevue: str,
    date_retour: str | None,
):
    """
    Email envoyé au propriétaire quand son livre est marqué comme rendu.
    """
    if not proprietaire_email:
        return

    sujet = f"Votre livre « {titre} » a été rendu"

    date_retour_txt = date_retour or "date de retour inconnue"

    contenu = (
        f"Bonjour {proprietaire},\n\n"
        f"Votre livre « {titre} » emprunté par {emprunteur} a été marqué comme rendu.\n\n"
        f"Emprunteur : {emprunteur}\n"
        f"Adresse email de l'emprunteur : {emprunteur_email}\n\n"
        f"Date d'emprunt : {date_emprunt}\n"
        f"Date de retour prévue : {date_retour_prevue}\n"
        f"Date de retour réelle : {date_retour_txt}\n\n"
        f"Si vous constatez un problème (livre abîmé, non rendu en réalité, etc.), "
        f"merci de le signaler au bureau du club.\n\n"
        f"Ceci est un message automatique envoyé par la bibliothèque du club."
    )

    envoyer_email(proprietaire_email, sujet, contenu)


def envoyer_mail_retour_emprunteur(
    proprietaire: str,
    proprietaire_email: str,
    emprunteur: str,
    emprunteur_email: str,
    titre: str,
    date_emprunt: str,
    date_retour_prevue: str,
    date_retour: str | None,
):
    """
    Email envoyé à l'emprunteur pour confirmer l'enregistrement du retour du livre.
    """
    if not emprunteur_email:
        return

    sujet = f"Retour enregistré pour « {titre} »"

    date_retour_txt = date_retour or "aujourd'hui"

    contenu = (
        f"Bonjour {emprunteur},\n\n"
        f"Le retour du livre « {titre} » a bien été enregistré dans la bibliothèque du club.\n\n"
        f"Propriétaire : {proprietaire}\n"
        f"Adresse email du propriétaire : {proprietaire_email}\n\n"
        f"Date d'emprunt : {date_emprunt}\n"
        f"Date de retour prévue : {date_retour_prevue}\n"
        f"Date de retour enregistrée : {date_retour_txt}\n\n"
        f"Merci d'avoir respecté le principe de partage des livres du Club Entrepreneurs.\n\n"
        f"Ceci est un message automatique envoyé par la bibliothèque du club."
    )

    envoyer_email(emprunteur_email, sujet, contenu)
