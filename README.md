# Air Paradise Chatbot - Prédiction et Réservation de Vols

## ✨ Introduction

Bienvenue dans le projet **Air Paradise Chatbot** ! Ce projet combine **Machine Learning, API Amadeus et un Chatbot** pour :

1. **Prédire les prix des vols** basés sur un ensemble de données fourni.
2. **Générer un dataset enrichi** avec les prix des vols.
3. **Permettre la réservation de vols via un chatbot interactif**.

---

## 📚 Structure du projet

```
📎 air_paradise_chatbot
├── 📂 data
│   ├── raw/                      # Données brutes non traitées
│   │   ├── dataset_vols.csv       # Dataset initial (sans prix)
│   ├── cleaned/                   # Données après nettoyage
│   │   ├── dataset_cleaned.csv     # Dataset nettoyé
│   ├── enriched/                   # Données enrichies avec prix
│   │   ├── dataset_vols_enrichi.csv
│   ├── prices_cache.db             # Base SQLite pour stockage des prix
├── 📂 notebooks
│   ├── 01_exploration.ipynb        # Analyse exploratoire (EDA)
│   ├── 02_preprocessing.ipynb      # Nettoyage et feature engineering
│   ├── 03_model_training.ipynb     # Entraînement du modèle ML
├── 📂 models
│   ├── flight_price_model.pkl  # Modèle ML entraîné
├── 📂 chatbot
│   ├── chatbot.py              # Code du chatbot
│   ├── intents.json            # Intentions du chatbot
│   ├── actions.py              # Actions personnalisées
├── 📂 api
│   ├── fetch_prices.py         # Script pour collecter les prix via Amadeus
│   ├── train_model.py          # Entraînement du modèle ML
│   ├── predict_prices.py       # Prédiction des prix
│   ├── db_cache.py             # Gestion du cache SQLite
├── 📂 web_app
│   ├── app.py                  # API Flask/FastAPI pour chatbot et prédictions
│   ├── templates/
│   │   ├── index.html          # Interface web utilisateur
│   ├── static/
│   │   ├── styles.css          # Styles CSS
├── 📂 tests
│   ├── test_fetch_prices.py    # Tests API Amadeus
│   ├── test_chatbot.py         # Tests du chatbot
│   ├── test_model.py           # Tests ML
├── download_dataset.py         # Script pour télécharger le dataset depuis Google Drive
├── .env                        # Variables d’environnement (API Keys)
├── .gitattributes              # Configuration des attributs Git
├── requirements.txt            # Librairies Python nécessaires
├── README.md                   # Documentation du projet
```

---

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-repo/air_paradise_chatbot.git
cd air_paradise_chatbot
```

### 2. Récupérer le dataset depuis Google Drive

Le dataset brut est stocké sur Google Drive. Pour le télécharger, utilisez le script `download_dataset.py` :

```bash
python download_dataset.py
```

Assurez-vous que le fichier est bien placé dans `data/raw/`.

### 3. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer l'API Amadeus

Créer un fichier `.env` et ajouter :

```env
API_KEY=VOTRE_CLE_API_AMADEUS
API_SECRET=VOTRE_SECRET_API_AMADEUS
```

---

## 📜 Configuration de `.gitattributes`

Un fichier `.gitattributes` est ajouté pour :
- Gérer les fins de ligne (`LF` vs `CRLF`) pour éviter les conflits entre Windows et Linux.
- Exclure certains fichiers binaires des différences (`diff`) Git.
- Gérer les fichiers volumineux via Git LFS.

Exemple de contenu du `.gitattributes` :

```gitattributes
# Normaliser les fins de ligne
* text=auto

# Ignorer les différences dans les fichiers binaires
*.pkl binary
*.pbix binary
*.db binary

# Gérer les fichiers volumineux avec Git LFS (si utilisé)
*.csv filter=lfs diff=lfs merge=lfs -text
*.json filter=lfs diff=lfs merge=lfs -text
```

---

## 💡 Utilisation

### 1. Récupérer des prix avec l’API Amadeus

```bash
python api/fetch_prices.py
```

### 2. Entraîner le modèle Machine Learning

```bash
python api/train_model.py
```

### 3. Générer 5M de prix avec le modèle ML

```bash
python api/predict_prices.py
```

### 4. Lancer le chatbot

```bash
python chatbot/chatbot.py
```

### 5. Lancer l'interface web (API Flask)

```bash
python web_app/app.py
```

Accédez à `http://127.0.0.1:5000/` dans votre navigateur.

---

## 🔧 Tests

Lancer les tests unitaires :

```bash
pytest tests/
```

---

## 🚀 Améliorations futures

- Ajouter des **options de paiement** directement via le chatbot.
- Améliorer l’algorithme de prédiction des prix avec **XGBoost**.
- Ajouter une interface utilisateur en **React.js**.

---

📢 **Félicitations, ton projet est maintenant fonctionnel !** 🚀

