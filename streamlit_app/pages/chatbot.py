import streamlit as st
st.set_page_config(page_title="💬 Chatbot Air Paradise", layout="centered")

import csv
import requests
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from langdetect import detect
from components.sidebar import display_sidebar

display_sidebar()

API_URL = "http://127.0.0.1:8000/chat"
PREDICT_URL = "http://127.0.0.1:8000/predict"

st.title("🤖 Smart Chatbot - Air Paradise")

st.markdown("""
    <style>
    .stTextInput > label, .stDateInput > label, .stTimeInput > label {
        font-weight: bold;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #f9f9f9;
        color: black;
    }
    .stChatMessageContent {
        color: black;
    }
    .main .block-container {
        color: black;
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
    }
</style>
""", unsafe_allow_html=True)

# Initialisation états session
for k, default in {"history": [], "infos_user": {}, "lang": "fr", "confirmation_demande": False}.items():
    if k not in st.session_state:
        st.session_state[k] = default

if st.session_state.history:
    last_user_msg = next((m["content"] for m in reversed(st.session_state.history) if m["role"] == "user"), "")
    st.session_state.lang = detect(last_user_msg)

is_en = st.session_state.lang.startswith("en")

# Fonction pour sauvegarder les messages
def save_message(role, message):
    with open("conversations.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), role, message])

# Affichage historique
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if prompt := st.chat_input("Ask your question or book a flight" if is_en else "Posez votre question ou réservez un vol"):
    st.session_state.history.append({"role": "user", "content": prompt})
    save_message("user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        history_msgs = [m["content"] for m in st.session_state.history if m["role"] == "user"]
        response = requests.post(API_URL, json={"message": prompt, "history": history_msgs})
        data = response.json()

        parsed = data.get("parsed", {})
        missing = data.get("missing", [])
        iata_codes = data.get("iata_codes", {})
        lang = data.get("lang", st.session_state.lang)

        st.session_state.lang = lang
        is_en = lang.startswith("en")
        st.session_state.infos_user.update({k: v for k, v in parsed.items() if v})
        save_message("user", prompt)

        st.session_state["iata_codes"] = iata_codes

        if "summary" in data:
            with st.chat_message("assistant"):
                st.markdown(data["summary"])
            st.session_state.history.append({"role": "assistant", "content": data["summary"]})
            save_message("assistant", data["summary"])

        if missing:
            msg = ("Here's what I still need to continue:\n" if is_en else "Voici ce qu'il me manque pour continuer :\n")
            msg += "\n".join(f"- {item}" for item in missing)
            with st.chat_message("assistant"):
                st.markdown(msg)
            st.session_state.history.append({"role": "assistant", "content": msg})

        if not missing and len(st.session_state.infos_user) >= 4 and not st.session_state.confirmation_demande:
            confirmation = ("Do you confirm this information?\n" if is_en else "Confirmez-vous ces informations ?\n")
            for k, v in st.session_state.infos_user.items():
                confirmation += f"- {k} : {v}\n"
            confirmation += ("\nPlease reply with 'ok', 'yes', 'correct' or fix what's wrong." if is_en else "\nVeuillez répondre avec \"ok\", \"parfait\" ou corrigez ce qui est faux.")
            st.session_state.confirmation_demande = True
            save_message
            with st.chat_message("assistant"):
                st.markdown(confirmation)
            st.session_state.history.append({"role": "assistant", "content": confirmation})

        if prompt.strip().lower() in ["ok", "yes", "d'accord", "parfait", "c'est bien ça", "c'est parfait", "super"] and st.session_state.confirmation_demande:
            try:
                heure_txt = st.session_state.infos_user.get("HEURE", "08:00")
                heure_obj = datetime.strptime(heure_txt, "%H:%M").time()
                origin_code = iata_codes.get("origin")
                destination_code = iata_codes.get("destination")
                payload = {
                    "DISTANCE": 0,
                    "SCHEDULED_TIME": int((datetime.combine(datetime.today(), heure_obj) - datetime.combine(datetime.today(), datetime.min.time())).seconds / 60),
                    "MONTH": datetime.today().month,
                    "DAY_OF_WEEK": datetime.today().weekday() + 1,
                    "ORIGIN_AIRPORT": origin_code,
                    "DESTINATION_AIRPORT": destination_code,
                    "SCHEDULED_DEPARTURE": heure_obj.strftime("%H:%M")
                }

                predict_resp = requests.post(PREDICT_URL, json=payload)
                predict_data = predict_resp.json()
                prix = predict_data.get("predicted_price")

                if prix is not None:
                    st.session_state["prix"] = prix
                    st.session_state["pret_a_reserver"] = True

                    origin_city = st.session_state.infos_user.get("ORIGIN_CITY", "")
                    destination_city = st.session_state.infos_user.get("DESTINATION_CITY", "")
                    origin_label = f"{origin_code} - {origin_city}"
                    destination_label = f"{destination_code} - {destination_city}"

                    st.session_state.update({
                        "origin_label": origin_label,
                        "destination_label": destination_label,
                        "date_vol": st.session_state.infos_user.get("DATE"),
                        "heure_vol": st.session_state.infos_user.get("HEURE")
                    })

                    prix_msg = f"💰 Estimated price: **{prix:.2f} USD**" if is_en else f"💰 Prix estimé : **{prix:.2f} USD**"
                    with st.chat_message("assistant"):
                        st.markdown(prix_msg)
                    st.session_state.history.append({"role": "assistant", "content": prix_msg})
                    save_message("assistant", prix_msg)
                else:
                    raise ValueError("Le prix n'a pas pu être calculé.")

            except Exception as e:
                err_msg = f"Prediction error: {e}" if is_en else f"Erreur lors de la prédiction : {e}"
                with st.chat_message("assistant"):
                    st.markdown(err_msg)
                st.session_state.history.append({"role": "assistant", "content": err_msg})

        if not st.session_state.get("pret_a_reserver") and not missing:
            extra = (
                "Do you have other questions about your flight? ✈️\nYou can ask:\n- Baggage rules\n- Check-in\n- Required documents\n- Customer support"
                if is_en else
                "Avez-vous d'autres questions ?\n\n🛆 Bagages\n🛫 Check-in\n🗘️ Documents requis\n📞 Support client"
            )
            st.session_state.history.append({"role": "assistant", "content": extra})
            save_message("assistant", extra)
            with st.chat_message("assistant"):
                st.markdown(extra)

    except Exception as e:
        st.session_state.history.append({"role": "assistant", "content": f" Erreur : {e}"})
        save_message("assistant", f"Erreur : {e}")

if st.session_state.get("pret_a_reserver"):
    if st.button("📩 Réserver ce vol maintenant"):
        switch_page("reservation")

st.markdown("---")
st.caption(" Powered by Gemini - Air Paradise © 2025 ")

