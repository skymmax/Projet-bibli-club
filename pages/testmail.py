import streamlit as st
from email_utils import envoyer_email

st.title("Test d'envoi d'email")

dest = st.text_input("Destinataire", value="ton.email@edu-devinci.fr")
sujet = st.text_input("Sujet", value="Test bibliothèque Club Entrepreneurs")
message = st.text_area("Message", value="Ceci est un test d'envoi d'email depuis Streamlit.")

if st.button("Envoyer le mail"):
    try:
        envoyer_email(dest, sujet, message)
        st.success("Email envoyé avec succès.")
    except Exception as e:
        st.error(f"Erreur lors de l'envoi : {e}")
