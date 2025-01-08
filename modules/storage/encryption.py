from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

ENCRYPTED_FOLDER = "encrypted_files/"

if not os.path.exists(ENCRYPTED_FOLDER):
    os.makedirs(ENCRYPTED_FOLDER)

# Derivar clave a partir del contenido del archivo
def derive_key_from_content(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return hashlib.sha256(file_content).digest()

# Cifrar un archivo
def encrypt_file(file_path):
    key = derive_key_from_content(file_path)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    encrypted_file_path = os.path.join(ENCRYPTED_FOLDER, os.path.basename(file_path) + ".enc")

    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)

    return {"success": True, "path": encrypted_file_path}

# Descifrar un archivo
def decrypt_file(encrypted_file_path, original_file_path):
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    key = derive_key_from_content(original_file_path)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    try:
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    except ValueError:
        return {"success": False, "message": "Error al descifrar el archivo."}

    decrypted_file_path = os.path.join("decrypted_files/", os.path.basename(original_file_path))
    if not os.path.exists("decrypted_files/"):
        os.makedirs("decrypted_files/")

    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    return {"success": True, "path": decrypted_file_path}