import streamlit as st
import os
from langdetect import detect

FAQ_PATH = r"C:\Users\ADMIN\Desktop\air_paradise_chatbot\data\rag\faq.txt"

@st.cache_data
def load_faq(path=FAQ_PATH):
    faq = {}
    current = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("[") and line.endswith("]\n"):
                    current = line[1:-2].strip().lower()
                    faq[current] = {"FR": "", "EN": ""}
                elif current and line.startswith("FR:"):
                    faq[current]["FR"] += line[3:].strip() + "\n"
                elif current and line.startswith("EN:"):
                    faq[current]["EN"] += line[3:].strip() + "\n"
    return faq

def display_sidebar():
    lang = st.session_state.get("lang", "fr")
    is_en = lang.startswith("en")

    st.sidebar.markdown("### 🌐 Langue / Language")
    if st.sidebar.button("Français"):
        st.session_state.lang = "fr"
    if st.sidebar.button("English"):
        st.session_state.lang = "en"

    faq_data = load_faq()
    lang_code = "EN" if is_en else "FR"

    st.sidebar.markdown("### 📖 FAQ" if not is_en else "### 📖 Help Topics")
    faq_options = [k for k in faq_data if faq_data[k][lang_code].strip()]
    selected = st.sidebar.selectbox("Choisissez une question :" if not is_en else "Select a question:", [""] + faq_options)

    if selected:
        content = faq_data[selected][lang_code].strip()
        if content:
            st.sidebar.markdown(f"**🔹 Réponse :**\n{content}" if not is_en else f"**🔹 Answer:**\n{content}")

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Réinitialiser la conversation" if not is_en else "🔄 Reset Conversation"):
        for key in ["history", "infos_user", "confirmation_demande", "prix", "origin_code", "destination_code", "origin_label", "destination_label", "date_vol", "heure_vol", "pret_a_reserver"]:
            st.session_state.pop(key, None)
        st.rerun()
