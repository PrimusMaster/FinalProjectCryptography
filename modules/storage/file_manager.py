import os
import hashlib
import shutil
from core.CoreCriptografico import *

# Ruta del almacenamiento simulado
CLOUD_STORAGE_DIR = "modules/storage/"

# Crear directorio de almacenamiento si no existe
os.makedirs(CLOUD_STORAGE_DIR, exist_ok=True)


def hash_file(file_path):
    """Genera el hash SHA-256 de un archivo."""
    with open(file_path, "rb") as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()


def upload_file(file_path):
    """
    Sube un archivo al almacenamiento simulado.
    Realiza cifrado y verifica duplicados.
    """
    if not os.path.exists(file_path):
        return {"success": False, "message": "El archivo no existe."}

    # Generar hash del archivo
    file_hash = hash_file(file_path)

    # Verificar si el archivo ya est� en la nube
    existing_files = os.listdir(CLOUD_STORAGE_DIR)
    if f"{file_hash}.enc" in existing_files:
        return {"success": False, "message": "Archivo duplicado encontrado."}

    # Cifrar y guardar el archivo
    encrypted_path = os.path.join(CLOUD_STORAGE_DIR, f"{file_hash}.enc")
    encrypt_file(file_path, encrypted_path)

    return {"success": True, "message": "Archivo subido exitosamente.", "path": encrypted_path}


def list_files():
    """Lista todos los archivos en el almacenamiento simulado."""
    return os.listdir(CLOUD_STORAGE_DIR)


def download_file(file_hash, output_path):
    """
    Descifra y descarga un archivo del almacenamiento.
    """
    encrypted_path = os.path.join(CLOUD_STORAGE_DIR, f"{file_hash}.enc")
    if not os.path.exists(encrypted_path):
        return {"success": False, "message": "Archivo no encontrado en la nube."}

    # Generar clave y descifrar archivo
    key = generate_key(encrypted_path)
    try:
        decrypt_file(encrypted_path, output_path)
        return {"success": True, "message": "Archivo descargado exitosamente."}
    except Exception as e:
        return {"success": False, "message": f"Error al descifrar: {e}"}


def delete_file(file_hash):
    """
    Elimina un archivo del almacenamiento simulado.
    """
    encrypted_path = os.path.join(CLOUD_STORAGE_DIR, f"{file_hash}.enc")
    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)
        return {"success": True, "message": "Archivo eliminado correctamente."}
    return {"success": False, "message": "Archivo no encontrado."}

def upload_(file_path):
    """
    Sube un archivo al almacenamiento simulado.
    Realiza cifrado y verifica duplicados.
    """
    if not os.path.exists(file_path):
        return {"success": False, "message": "El archivo no existe."}

    # Generar hash del archivo
    file_hash = hash_file(file_path)

    # Verificar si el archivo ya está en la nube
    existing_files = os.listdir(CLOUD_STORAGE_DIR)
    if f"{file_hash}.enc" in existing_files:
        return {"success": False, "message": "Archivo duplicado encontrado."}

    # Cifrar y guardar el archivo
    encrypted_path = os.path.join(CLOUD_STORAGE_DIR, f"{file_hash}.enc")
    encrypt_file(file_path, encrypted_path)

    return {"success": True, "message": "Archivo subido exitosamente.", "path": encrypted_path}
