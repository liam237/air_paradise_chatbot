import streamlit as st
st.set_page_config(page_title="Air Paradise", layout="centered")

import pandas as pd
import requests
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
import os
from components.sidebar import display_sidebar

API_URL = "http://127.0.0.1:8000"

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

display_sidebar()

st.title("Air Paradise ✈️ Réservation et Estimation de Vols")

# Message si redirigé depuis le chatbot
if st.session_state.get("redirected_from_chat"):
    st.info("Vous avez été redirigé ici pour compléter votre demande de vol." if st.session_state.lang == "fr" else "You’ve been redirected here to complete your flight request.")
    st.session_state["redirected_from_chat"] = False

# Affichage du logo
logo_path = r"C:/Users/ADMIN/Desktop/air_paradise_chatbot/streamlit_app/assets/images/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=180)

# Charger le mapping des aéroports
mapping_path = r"C:/Users/ADMIN/Desktop/air_paradise_chatbot/data/mapping/airport_mapping.csv"
airport_mapping = pd.read_csv(mapping_path)

# Préparer les options complètes pour autocomplétion
airport_mapping['COMBO'] = airport_mapping.apply(
    lambda r: f"{r['IATA_CODE']} - {r['AIRPORT']} ({r['CITY']}, {r['COUNTRY']})", axis=1
)
all_options = airport_mapping['COMBO'].tolist()

st.subheader("1. Sélection du vol")

# Sélection départ et arrivée
col1, col2 = st.columns(2)
with col1:
    chosen_depart = st.selectbox("Aéroport de départ", all_options, key="depart_select")
    origin_code = chosen_depart.split(" - ")[0] if chosen_depart else None

with col2:
    chosen_arrivee = st.selectbox("Aéroport de destination", all_options, key="arrivee_select")
    destination_code = chosen_arrivee.split(" - ")[0] if chosen_arrivee else None

# Date et heure
col3, col4 = st.columns(2)
with col3:
    date_vol = st.date_input("Date du vol", datetime.today())
with col4:
    heure_vol = st.text_input("Heure prévue de départ (HH:MM)", "08:00")

# Bouton de prédiction
if st.button(" Estimer le prix du vol", key="predict_button"):
    if origin_code and destination_code and heure_vol:
        try:
            heure = datetime.strptime(heure_vol, "%H:%M").time()
            payload = {
                "DISTANCE": 0,
                "SCHEDULED_TIME": int((datetime.combine(datetime.today(), heure) - datetime.combine(datetime.today(), datetime.min.time())).seconds / 60),
                "MONTH": date_vol.month,
                "DAY_OF_WEEK": date_vol.weekday() + 1,
                "ORIGIN_AIRPORT": origin_code,
                "DESTINATION_AIRPORT": destination_code,
                "SCHEDULED_DEPARTURE": heure.strftime("%H:%M")
            }
            resp = requests.post(f"{API_URL}/predict", json=payload)
            result = resp.json()
            prix = result.get('predicted_price')

            st.session_state['prix'] = prix
            st.session_state['origin_code'] = origin_code
            st.session_state['origin_label'] = chosen_depart
            st.session_state['destination_code'] = destination_code
            st.session_state['destination_label'] = chosen_arrivee
            st.session_state['date_vol'] = str(date_vol)
            st.session_state['heure_vol'] = heure_vol
            st.session_state['pret_a_reserver'] = True

            st.success(f"💵 Prix estimé : {prix} USD")

        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")
    else:
        st.warning("❗ Merci de sélectionner un aéroport de départ, d'arrivée, et une heure valide.")

# Redirection vers réservation
if st.session_state.get('pret_a_reserver'):
    if st.button("Oui, je veux réserver ce vol"):
        switch_page("reservation")

st.markdown("---")
st.caption("Air Paradise © 2025")
