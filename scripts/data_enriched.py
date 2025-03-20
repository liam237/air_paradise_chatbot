import pandas as pd
import numpy as np

# Charger le dataset
DATASET_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/cleaned/dataset_cleaned.csv"
df = pd.read_csv(DATASET_PATH)

# Liste des compagnies standard (exclut low-cost et premium)
standard_airlines = ["MQ", "EV", "OO", "HA", "WN", "US", "B6", "AS", "VX"]

# Filtrer uniquement les vols des compagnies standard
df_standard = df[df["AIRLINE"].isin(standard_airlines)].copy()

# Liste des grands aéroports (plus chers en moyenne)
big_airports = ["JFK", "LAX", "ORD", "DFW", "ATL", "MIA", "SFO", "SEA", "DEN", "BOS"]

# Fonction améliorée pour générer un prix réaliste
def generate_price(row):
    base_price = (row["DISTANCE"] * 0.12) + (row["SCHEDULED_TIME"] * 0.5)  

    # Facteur saisonnier
    saison_factor = 1.2 if row["MONTH"] in [6, 7, 8, 12] else 1.0  

    # Facteur week-end
    week_factor = 1.15 if row["DAY_OF_WEEK"] in [5, 7] else 1.0  

    # Facteur heure de départ
    try:
        hour = int(row["SCHEDULED_DEPARTURE"].split(":")[0])
        hour_factor = 1.1 if hour < 6 or hour > 20 else 1.0  
    except:
        hour_factor = 1.0  # Sécurité en cas d'erreur

    # Facteur aéroport
    airport_factor = 1.15 if row["ORIGIN_AIRPORT"] in big_airports else 1.0  

    # Facteur dernière minute
    last_minute_factor = 1.3 if row["DAY"] <= 7 else 1.0  

    # Facteur escales basé sur la vitesse moyenne
    speed = row["DISTANCE"] / row["SCHEDULED_TIME"] if row["SCHEDULED_TIME"] > 0 else np.nan
    if speed < 8:
        stops_factor = 1.3  # Vol avec au moins 1 escale
    elif speed < 12:
        stops_factor = 1.1  # Vol avec possible escale
    else:
        stops_factor = 1.0  # Vol direct

    # Ajout d'une variation aléatoire réaliste
    random_factor = np.random.uniform(0.9, 1.2)  

    # Appliquer les facteurs
    final_price = base_price * saison_factor * week_factor * hour_factor * airport_factor * last_minute_factor * stops_factor * random_factor

    # Limites pour éviter les valeurs absurdes
    final_price = max(50, min(final_price, 2500))  

    return round(final_price, 2)  

# Appliquer la fonction sur tout le dataset
df_standard["PRICE_USD"] = df_standard.apply(generate_price, axis=1)

# Sauvegarde du dataset complet
PRICES_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/enriched/data_enriched.csv"
df_standard.to_csv(PRICES_PATH, index=False)

print(f"[INFO] Génération des prix terminée Fichier enregistré : {PRICES_PATH}")

import pandas as pd
import numpy as np

# Charger le dataset
import pandas as pd
import numpy as np
DATASET_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/enriched/data_enriched.csv"
df = pd.read_csv(DATASET_PATH)
print(df[["DISTANCE", "SCHEDULED_TIME", "PRICE_USD"]].describe())
print(df[df["PRICE_USD"] > 2000])
