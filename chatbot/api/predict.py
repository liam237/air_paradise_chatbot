import pandas as pd
from category_encoders import HashingEncoder
from chatbot.api.model_loader import load_model

# Charger le modèle ML une seule fois
model = load_model()

# Initialiser le même HashingEncoder qu'à l'entraînement
hash_encoder = HashingEncoder(n_components=8)

def categorize_time(time_str: str) -> str:
    """
    Transforme une heure (HH:MM) en une catégorie (matin, journee, soir).
    """
    try:
        hour = int(time_str.split(":")[0])
        if hour < 6:
            return "matin"
        elif hour < 18:
            return "journee"
        else:
            return "soir"
    except Exception:
        return "journee"  # par défaut si l'heure est mal formée

def preprocess_input(data: dict) -> pd.DataFrame:
    """
    Prépare les données utilisateur pour correspondre aux attentes du modèle ML.
    """
    df = pd.DataFrame([data])

    # Encodage des aéroports avec hashing
    hashed = hash_encoder.fit_transform(df[["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]])
    df = pd.concat([df, hashed], axis=1)
    df.drop(columns=["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"], inplace=True)

    # Transformation de l'heure en période
    df["DEPARTURE_PERIOD"] = df["SCHEDULED_DEPARTURE"].apply(categorize_time)
    df = pd.get_dummies(df, columns=["DEPARTURE_PERIOD"], drop_first=True)
    df.drop(columns=["SCHEDULED_DEPARTURE"], inplace=True)

    # Sécuriser les colonnes manquantes après get_dummies
    for col in ["DEPARTURE_PERIOD_matin", "DEPARTURE_PERIOD_soir"]:
        if col not in df.columns:
            df[col] = 0

    # Renommer les colonnes du hashing pour matcher : col_0 → col_7
    hashed_cols = [col for col in df.columns if col.startswith("ORIGIN_") or col.startswith("DESTINATION_")]
    if len(hashed_cols) == 8:
        df.rename(columns={c: f"col_{i}" for i, c in zip(hashed_cols, range(8))}, inplace=True)

    # Ordre des colonnes attendu par le modèle
    expected_cols = [
        "DISTANCE", "SCHEDULED_TIME", "MONTH", "DAY_OF_WEEK",
        "col_0", "col_1", "col_2", "col_3",
        "col_4", "col_5", "col_6", "col_7",
        "DEPARTURE_PERIOD_matin", "DEPARTURE_PERIOD_soir"
    ]

    # Ajouter les colonnes manquantes si nécessaire
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_cols]
    return df

def predict_price(payload: dict) -> float:
    """
    Exécute la prédiction de prix sur la base des données utilisateur.
    """
    try:
        processed_data = preprocess_input(payload)
        prediction = model.predict(processed_data)[0]
        return round(float(prediction), 2)
    except Exception as e:
        raise RuntimeError(f"[ERREUR - Prédiction] : {str(e)}")
