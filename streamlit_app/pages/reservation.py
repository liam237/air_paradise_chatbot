import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import smtplib
from email.message import EmailMessage
import os
import qrcode
import random
import string

st.set_page_config(page_title="Réservation de vol - Air Paradise", layout="centered")
st.markdown("""
    <style>
        .stTextInput > label, .stDateInput > label, .stTimeInput > label {
            font-weight: bold;
        }
        .stTextInput input, .stTextArea textarea {
            background-color: #f9f9f9;
        }
        .stButton > button {
            background-color: #0183f5;
            color: white;
            font-weight: bold;
        }
        .stApp {
            background-image: url("https://www.francebleu.fr/s3/cruiser-production/2023/06/f21ac4df-5c79-4db6-9152-9b59aaa87aeb/1200x680_sc_gettyimages-1435906430.webp");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
    </style>
""", unsafe_allow_html=True)

st.title("Réservation de votre vol")

logo_path = r"C:\Users\ADMIN\Desktop\air_paradise_chatbot\streamlit_app\assets\images\logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=180)

prix = st.session_state.get("prix")
origin = st.session_state.get("origin_label")
destination = st.session_state.get("destination_label")
date_vol = st.session_state.get("date_vol")
heure_vol = st.session_state.get("heure_vol")

if not prix:
    st.error("Aucune estimation de vol en cours. Veuillez d'abord passer par la page d'estimation.")
    st.stop()

with st.container():
    st.subheader("Détails du vol")
    st.markdown(f"**De** : {origin}")
    st.markdown(f"**À** : {destination}")
    st.markdown(f"**Date** : {date_vol}")
    st.markdown(f"**Heure** : {heure_vol}")
    st.markdown(f"**Prix estimé** : {round(prix, 2)} USD")

st.markdown("---")

with st.container():
    st.subheader("👤 Informations passager")
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("👤 Nom complet")
        email = st.text_input("📧 Adresse email")
        telephone = st.text_input("📱 Numéro de téléphone")
    with col2:
        passeport = st.text_input("🛂 Numéro de passeport")
        rib = st.text_input("🏦 RIB (Paiement)")

if st.button("✅ Confirmer et générer le billet"):
    if not all([nom.strip(), email.strip(), telephone.strip(), passeport.strip(), rib.strip()]):
        st.warning("Merci de remplir tous les champs obligatoires.")
    else:
        st.session_state["infos_validées"] = True
        st.session_state["nom"] = nom
        st.session_state["email"] = email
        st.session_state["telephone"] = telephone
        st.session_state["passeport"] = passeport
        st.session_state["rib"] = rib

if st.session_state.get("infos_validées"):
    with st.expander("Vérifier les informations du billet"):
        st.markdown(f"**Nom** : {st.session_state['nom']}")
        st.markdown(f"**Passeport** : {st.session_state['passeport']}")
        st.markdown(f"**Email** : {st.session_state['email']}")
        st.markdown(f"**Téléphone** : {st.session_state['telephone']}")
        st.markdown(f"**Vol de** {origin} **vers** {destination}")
        st.markdown(f"**Date** : {date_vol} | **Heure** : {heure_vol}")
        st.markdown(f"**Prix** : {round(prix, 2)} USD")

    if st.button("💳 Payer et recevoir mon billet"):
        siege = f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
        code_vol = "AP" + ''.join(random.choices(string.digits, k=4))
        num_embarquement = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        qr_info = f"Nom: {st.session_state['nom']}\nVol: {code_vol}\nEmbarquement: {num_embarquement}\nDe: {origin}\nÀ: {destination}\nDate: {date_vol}\nHeure: {heure_vol}\nSiège: {siege}\nPrix: {round(prix, 2)} USD"
        qr = qrcode.make(qr_info)
        qr_path = "temp_qr.png"
        qr.save(qr_path)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Air Paradise - Billet d'avion", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Nom: {st.session_state['nom']}", ln=True)
        pdf.cell(200, 10, txt=f"Passeport: {st.session_state['passeport']}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {st.session_state['email']}", ln=True)
        pdf.cell(200, 10, txt=f"Téléphone: {st.session_state['telephone']}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Vol: {code_vol}", ln=True)
        pdf.cell(200, 10, txt=f"Embarquement: {num_embarquement}", ln=True)
        pdf.cell(200, 10, txt=f"Siège: {siege}", ln=True)
        pdf.cell(200, 10, txt=f"De: {origin}", ln=True)
        pdf.cell(200, 10, txt=f"À: {destination}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {date_vol}", ln=True)
        pdf.cell(200, 10, txt=f"Heure: {heure_vol}", ln=True)
        pdf.cell(200, 10, txt=f"Prix: {round(prix, 2)} USD", ln=True)
        pdf.image(qr_path, x=70, y=pdf.get_y() + 10, w=60)

        pdf_bytes = pdf.output(dest='S').encode('latin1')

        st.download_button(
            "📄 Télécharger le billet PDF",
            data=pdf_bytes,
            file_name="billet_air_paradise.pdf",
            mime="application/pdf"
        )

        try:
            msg = EmailMessage()
            msg['Subject'] = "Confirmation de réservation - Air Paradise"
            msg['From'] = st.secrets["EMAIL"]
            msg['To'] = st.session_state['email']
            msg.set_content(f"Bonjour {st.session_state['nom']},\n\nVous trouverez ci-joint votre billet d'avion Air Paradise.\n\nMerci de voyager avec nous ✈️")
            msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='billet_air_paradise.pdf')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(st.secrets["EMAIL"], st.secrets["APP_PASSWORD"])
                smtp.send_message(msg)

            st.success("✉️ Email envoyé avec succès !")

        except Exception as e:
            st.error(f"Erreur lors de l'envoi de l'email : {e}")

        if os.path.exists(qr_path):
            os.remove(qr_path)

