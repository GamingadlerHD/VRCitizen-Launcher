import os
import zipfile
import tempfile
import subprocess
import requests

from constants import VORPX_URL

def update_vorpx():
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "download.zip")

    # ZIP-Datei herunterladen
    response = requests.get(VORPX_URL, timeout=150)
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # ZIP entpacken
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # .exe-Datei finden und ausführen
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".exe"):
                exe_path = os.path.join(root, file)
                subprocess.run([exe_path], shell=True, check=True)
                break
