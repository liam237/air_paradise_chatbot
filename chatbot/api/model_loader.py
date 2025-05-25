# chatbot/api/model_loader.py

import joblib
from pathlib import Path

MODEL_PATH = Path(r"C:\Users\ADMIN\Desktop\air_paradise_chatbot\models\best_flight_price_model.pkl")

def load_model():
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(f"[ERREUR] Impossible de charger le modèle : {e}")
