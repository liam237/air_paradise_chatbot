import pandas as pd
import joblib


model = joblib.load("C:\\Users\\ADMIN\\Desktop\\air_paradise_chatbot\\models\\best_flight_price_model.pkl")


# Charger un exemple de données à prédire
file_path = "C:\\Users\\ADMIN\\Desktop\\air_paradise_chatbot\\data\\final\\final_dataset.csv"
df = pd.read_csv(file_path)

# Supposons que la colonne cible soit "PRICE_USD", on enlève cette colonne
X = df.drop(columns=["PRICE_USD"], errors="ignore")

# Prédire les prix des billets d'avion
predictions = model.predict(X)

# Afficher les prédictionsà
print(predictions)
