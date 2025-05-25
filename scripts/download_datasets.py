import gdown
import os

# Dictionnaire associant l'ID Google Drive, le chemin de destination et le nom de fichier
files_to_download = {
    # Fichier 1 → data/raw
    "18fYgHXaqQ8yWLXl2Zfj_KTt5ohd6hbgK": os.path.join("data", "raw", "dataset_raw.csv"),
    # Fichier 2 → data/cleaned
    "1Ira33RQ8KWBIr-O8UMjPDw18tDAb9abu": os.path.join("data", "cleaned", "dataset_cleaned.csv"),
    # Fichier 3 → data/cleaned (deuxième fichier dans ce dossier)
    "1zwZvpbtEbTJY-qZYe0yRpNhGUk6YMUnn": os.path.join("data", "cleaned", "dataset_cleaned_standard.csv"),
    # Fichier 4 → data/enriched
    "1mNQr1raaJ62EBn0t-9HOLgWMqr8hqYEq": os.path.join("data", "enriched", "dataset_enriched.csv"),
    # Fichier 5 → data/final
    "1NMlubNXleu0mPexsmQzFDW5v6rz5O87Q": os.path.join("data", "final", "dataset_final.csv"),
    # Fichier 6 → data/final (deuxième fichier dans ce dossier)
    "1ynvgoSYV3Mwy-mIjvadazGmzVdeAMUGV": os.path.join("data", "final", "dataset_cleaned_standard_with_predictions.csv")

}

# Téléchargement de chaque fichier
for file_id, output_path in files_to_download.items():
    # Créer le dossier de destination s'il n'existe pas
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[INFO] Téléchargement du fichier vers : {output_path}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

print("[INFO] Tous les fichiers ont été téléchargés avec succès !")
