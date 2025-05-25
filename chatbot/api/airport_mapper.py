import pandas as pd
from pathlib import Path

DATA_PATH = Path("C:\\Users\\ADMIN\Desktop\\air_paradise_chatbot\\data\\mapping\\airport_mapping.csv")

def load_airport_data():
    """
    Charge le fichier CSV contenant les informations des aéroports.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"⚠️ Fichier introuvable : {DATA_PATH}")
    except Exception as e:
        raise RuntimeError(f"Erreur de chargement : {str(e)}")

def get_airport_info(code: str):
    """
    Retourne les informations de l'aéroport correspondant à un code IATA.
    """
    df = load_airport_data()

    # Nettoyage : supprime les espaces et met en majuscules
    df["IATA_CODE"] = df["IATA_CODE"].astype(str).str.strip().str.upper()
    code = code.strip().upper()

    row = df[df["IATA_CODE"] == code]

    if row.empty:
        return {"error": f"Aucun aéroport trouvé pour le code {code}"}
    else:
        info = row.iloc[0]
        return {
            "IATA": info.get("IATA_CODE", code),
            "Name": info.get("AIRPORT", "Inconnu"),
            "City": info.get("CITY", "Inconnue"),
            "Country": info.get("COUNTRY", "Inconnu")
        }
