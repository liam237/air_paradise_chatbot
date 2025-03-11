import gdown
import os

# ID du fichier flights.csv sur Google Drive
FILE_ID = "18fYgHXaqQ8yWLXl2Zfj_KTt5ohd6hbgK"
OUTPUT_PATH = "data/raw/flights.csv"

# Créer le dossier s'il n'existe pas
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Télécharger le fichier depuis Google Drive
URL = f"https://drive.google.com/uc?id={FILE_ID}"
gdown.download(URL, OUTPUT_PATH, quiet=False)

print(f" Dataset téléchargé avec succès : {OUTPUT_PATH}")
