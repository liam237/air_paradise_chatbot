import gdown
import os

# Dictionnaire associant l'ID Google Drive, le chemin de destination et le nom de fichier
files_to_download = {
    # Fichier 1 → data/mapping
    "1KW28vEa5mKfudR6lqMsKmrnmziRQ8PMG": os.path.join("data", "mapping", "airport_mapping.csv"),
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