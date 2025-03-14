import pandas as pd
import numpy as np

# Charger les données
DATASET_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/cleaned/dataset_cleaned.csv"
df = pd.read_csv(DATASET_PATH)

# Liste des grands aéroports (plus chers en moyenne)
big_airports = ["JFK", "LAX", "ORD", "DFW", "ATL", "MIA", "SFO", "SEA", "DEN", "BOS"]

# Fonction améliorée pour générer un prix réaliste
def generate_price(row):
    base_price = (row["DISTANCE"] * 0.12) + (row["ELAPSED_TIME"] * 0.5)  # Distance et durée influencent le prix

    # Facteur saisonnier (haute saison)
    saison_factor = 1.2 if row["MONTH"] in [6, 7, 8, 12] else 1.0  

    # Facteur compagnie aérienne (low-cost vs premium)
    low_cost = ["NK", "F9", "G4"]  # Spirit, Frontier, Allegiant
    premium = ["AA", "DL", "UA"]  # American, Delta, United
    if row["AIRLINE"] in low_cost:
        airline_factor = 0.8  # -20% pour les low-cost
    elif row["AIRLINE"] in premium:
        airline_factor = 1.1  # +10% pour les compagnies premium
    else:
        airline_factor = 1.0  

    # Facteur week-end (vendredi et dimanche plus chers)
    week_factor = 1.15 if row["DAY_OF_WEEK"] in [5, 7] else 1.0  

    # Facteur heure de départ (vols matin et soir plus chers)
    hour = int(row["SCHEDULED_DEPARTURE"].split(":")[0])
    hour_factor = 1.1 if hour < 6 or hour > 20 else 1.0  

    # Facteur aéroport (grands aéroports plus chers)
    airport_factor = 1.2 if row["ORIGIN_AIRPORT"] in big_airports else 1.0  

    # Facteur de dernière minute (vols dans les 7 jours)
    last_minute_factor = 1.3 if row["DAY"] <= 7 else 1.0  

    # Facteur escales (vols directs plus chers)
    stops_factor = 1.2 if row["DISTANCE"] > 2500 else 1.0  

    # Ajout d'une variation aléatoire réaliste
    random_factor = np.random.uniform(0.9, 1.2)  

    # Appliquer les facteurs
    final_price = base_price * saison_factor * airline_factor * week_factor * hour_factor * airport_factor * last_minute_factor * stops_factor * random_factor

    # Limites pour éviter les valeurs absurdes
    if final_price < 50:  
        final_price = 50  
    if final_price > 2000 and row["DISTANCE"] < 3000:  
        final_price = 2000  

    return round(final_price, 2)  

# Appliquer la fonction à chaque ligne du dataset
df["PRICE_USD"] = df.apply(generate_price, axis=1)

# Sauvegarder le dataset avec les prix réalistes
PRICES_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/enriched/data_enriched_realistic.csv"
df.to_csv(PRICES_PATH, index=False)

print(f"[INFO] Prix réalistes générés et enregistrés dans {PRICES_PATH}")
