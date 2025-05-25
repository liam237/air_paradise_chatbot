import streamlit as st
import os

st.set_page_config(page_title="Bienvenue chez Air Paradise", layout="centered", page_icon="🌤️")
st.markdown(
    """
    <style>
        .stApp {
            background-image: url("https://www.francebleu.fr/s3/cruiser-production/2023/06/f21ac4df-5c79-4db6-9152-9b59aaa87aeb/1200x680_sc_gettyimages-1435906430.webp");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .stSuccess {
            font-weight: regular;
            font-size: 20px;
            color: #ffffff;
        }
        .stButton > button {
            background-color: #0183f5;
            color: white;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the logo
logo_path = r"c:\users\admin\desktop\air_paradise_chatbot\streamlit_app\assets\images\logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)

st.title("🇺🇸 Air Paradise - votre compagnie aérienne 100% USA")

st.markdown("""
Bienvenue chez **Air Paradise**, la compagnie aérienne d'excellence pour vos trajets aux **États-Unis**. 

### Notre mission est simple : vous offrir des vols fiables, confortables, au **meilleur prix prédit** par nos algorithmes intelligents. 

### Avec notre nouveau chatbot intelligent, réservez vos billets en quelques clics, recevez un QR code électronique, et recevez votre **billet PDF par email** instantanément ! ✈️

---

#### - Prévision intelligente des prix
Notre IA vous indique le **meilleur tarif estimé** pour votre vol, en fonction de l'heure, la date, la distance et la saison.

#### - Réservation facile & sécurisée
Nous collectons vos informations de manière confidentielle, avec validation biométrique et confirmation par email.

#### - Billet numérique avec QR code
Un QR personnalisé vous est remis, scannable à tout moment !

---

""")

st.success("Prêt à explorer le ciel américain ?")
st.markdown("### Que souhaitez-vous faire ?")

if st.button("🎟️ Démarrer une prédiction avec notre chatbot"):
    from streamlit_extras.switch_page_button import switch_page
    switch_page("chatbot")

if st.button("🎟️ Utiliser notre formulaire"):
    from streamlit_extras.switch_page_button import switch_page
    switch_page("interface")

# More button styling (as per your requirement)
st.markdown(
    """
    <style>
        .stbutton {
            background-color: #45a049; /* Changed the second button color */
            color: white; 
            font-size: 18px;
            padding: 10px 20px; 
            border-radius: 5px; 
        }
    </style>
    """,
    unsafe_allow_html=True
)