import pandas as pd
import numpy as np

DATASET_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/cleaned/dataset_cleaned.csv"
df = pd.read_csv(DATASET_PATH)

#  Liste des aéroports avec une forte demande (plus chers en moyenne)
big_airports = ["JFK", "LAX", "ORD", "DFW", "ATL", "MIA", "SFO", "SEA", "DEN", "BOS"]

# Fonction pour générer un prix réaliste
def generate_price(row):
    
    base_price = (row["DISTANCE"] * 0.12) + (row["ELAPSED_TIME"] * 0.5)  # Distance et durée influencent le prix

    # Facteur saisonnier
    saison_factor = 1.2 if row["MONTH"] in [6, 7, 8, 12] else 1.0  

    # Facteur compagnie aérienne
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
    hour = int(row["SCHEDULED_DEPARTURE"].split(":")[0])  # Extraire l'heure
    if hour < 6 or hour > 20:
        hour_factor = 1.1  # Vols matinaux ou tardifs +10%
    else:
        hour_factor = 1.0  

    # Facteur aéroport (les plus grands sont plus chers)
    airport_factor = 1.2 if row["ORIGIN_AIRPORT"] in big_airports else 1.0  

    # Ajout d'une variation aléatoire
    random_factor = np.random.uniform(0.9, 1.2)  

    # Calcul du prix final
    final_price = base_price * saison_factor * airline_factor * week_factor * hour_factor * airport_factor * random_factor
    return round(final_price, 2)  

# Appliquer la fonction à chaque ligne du dataset
df["PRICE_USD"] = df.apply(generate_price, axis=1)

# Sauvegarder le dataset avec les prix générés
PRICES_PATH = "D:/Projet_AirParadise/air_paradise_chatbot/data/enriched/data_enriched.csv"
df.to_csv(PRICES_PATH, index=False)

print(f"[INFO] Prix générés et enregistrés dans {PRICES_PATH}")

import pandas as pd
import numpy as np
df = pd.read_csv("D:/Projet_AirParadise/air_paradise_chatbot/data/enriched/dataset_enriched.csv")
print(df.describe())