import smtplib
from email.message import EmailMessage
import streamlit as st


def envoyer_email(destinataire: str, sujet: str, contenu_texte: str):
    """
    Envoie un email texte simple via la configuration SMTP définie dans st.secrets.
    """

    smtp_user = st.secrets["SMTP_USER"]
    smtp_password = st.secrets["SMTP_PASSWORD"]
    smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(st.secrets.get("SMTP_PORT", 587))
    from_name = st.secrets.get("FROM_NAME", "Bibliothèque Club Entrepreneurs")

    msg = EmailMessage()
    msg["Subject"] = sujet
    msg["From"] = f"{from_name} <{smtp_user}>"
    msg["To"] = destinataire
    msg.set_content(contenu_texte)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
