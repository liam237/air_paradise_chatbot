import gdown
import os

# Dictionnaire associant l'ID Google Drive au chemin de destination
files_to_download = {
    # Ton fichier `.pkl` → models/
    "1yCpY3AaK2LlGuL4BYbHAykBEtyC1B69b": os.path.join("models", "best_flight_price_model.pkl")
}

# Téléchargement de chaque fichier
for file_id, output_path in files_to_download.items():
    # Créer le dossier de destination s'il n'existe pas
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[INFO] Téléchargement du fichier vers : {output_path}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

print("[INFO] Le fichier a été téléchargé avec succès !")