
# Air Paradise – Flight Booking Chatbot

**Air Paradise** est une application web intelligente permettant de rechercher, estimer et réserver des vols internes aux États-Unis à l’aide d’un chatbot propulsé par l’IA.

---

## Fonctionnalités principales

- Chatbot multilingue (FR / EN) intelligent basé sur **Gemini AI**
- Prédiction du prix de vol selon date, heure, aéroports, distance
- Formulaire manuel alternatif de réservation
- Génération de billet PDF avec QR Code
- Envoi du billet par email
- Sidebar FAQ avec recherche contextuelle

---

## Technologies utilisées

###  Backend (API)
- **FastAPI** : framework léger pour servir les prédictions
- **Pydantic** : validation des entrées via `PredictionRequest`
- **joblib** : chargement du modèle ML (`.pkl`)
- **requests** : communication frontend/backend

### Machine Learning
- **scikit-learn** : modèle de régression
- **category_encoders** : encodage hashing des aéroports
- **pandas** : preprocessing & dataframe

### Intelligence conversationnelle
- **Google Generative AI (Gemini)** : extraction de slots conversationnels
- **langdetect** + **dateparser** : pour comprendre l'utilisateur naturellement

### Frontend (App)
- **Streamlit** : framework pour l'interface utilisateur
- **streamlit_extras** : `switch_page_button`, amélioration UX
- **FPDF** / **qrcode** : génération de billets PDF avec QR code

---

## Arborescence simplifiée

```
air_paradise_chatbot
 ┣ api/                      # Backend FastAPI
 ┣ streamlit_app/           # App utilisateur (chatbot, interface, réservation)
 ┣ data/                    # mapping + contexte + faq
 ┣ models/                  # modèle ML exporté (.pkl)
 ┣ notebooks/               # notebooks Jupyter (exploration, preprocessing, training)
 ┣ tests/                   # fichiers de conversation sauvegardés
 ┣ main.py                   # Point d'entrée API
 ┗ README.md                 # Ce fichier
```

---

## Démarrage rapide

### 1. Lancer l'API
```bash
uvicorn main:app --reload
```

### 2. Lancer l’application
```bash
streamlit run streamlit_app/pages/home.py
```

---

## Fichiers de prédiction utilisés

Les notebooks suivants détaillent l’approche ML :
- `01_exploration.ipynb` : visualisation initiale
- `02_preprocessing.ipynb` : nettoyage + encodage
- `Select_variables.ipynb` : sélection des features clés
- `03_model_training.ipynb` : régression + évaluation
- `04_mapping.ipynb` : enrichissement des aéroports

---

## Statut

-  Fonctionnalités principales terminées
-  Conversation sauvegardée dans `tests/conversations.csv`
-  Code nettoyé et structuré

---

##  Idées futures

- Connexion à une base de données pour réservations
- Tableau de bord admin (Streamlit ou Dash)
- Version vocale (Speech-to-Text)
- Statistiques sur les demandes (analyse NLP)

---

##  Auteurs
Fonkui william
Temgoua carine
Kenfack Ariol

---

**© Air Paradise 2025**
