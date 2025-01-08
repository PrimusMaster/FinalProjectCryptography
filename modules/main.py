import os
import sqlite3
from tkinter import *
from tkinter import messagebox
from storage import *
from  storage.file_manager import *
from  storage.encryption import *
# Crear base de datos para usuarios
DB_PATH = "users.db"

if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """)
        conn.commit()

def decrypt_document(frame):
    frame.destroy()
    frameDecrypt = Frame(root)

    Label(frameDecrypt, text="Ruta del archivo cifrado:").grid(row=0, column=0)
    encryptedFileEntry = Entry(frameDecrypt, width=30)
    encryptedFileEntry.grid(row=0, column=1)

    Label(frameDecrypt, text="Ruta del archivo original (para clave):").grid(row=1, column=0)
    originalFileEntry = Entry(frameDecrypt, width=30)
    originalFileEntry.grid(row=1, column=1)

    def decrypt():
        encrypted_path = encryptedFileEntry.get()
        original_path = originalFileEntry.get()

        if not os.path.exists(encrypted_path):
            messagebox.showerror("Error", "El archivo cifrado no existe.")
            return

        if not os.path.exists(original_path):
            messagebox.showerror("Error", "El archivo original no existe.")
            return

        response = decrypt_file(encrypted_path, original_path)
        if response["success"]:
            messagebox.showinfo("Éxito", f"Archivo descifrado correctamente: {response['path']}")
            generate_Login(frameDecrypt)
        else:
            messagebox.showerror("Error", response["message"])

    decryptButton = Button(frameDecrypt, text="Descifrar", command=decrypt)
    decryptButton.grid(row=2, column=0, columnspan=2)

    backButton = Button(frameDecrypt, text="Volver", command=lambda: generate_Login(frameDecrypt))
    backButton.grid(row=3, column=0, columnspan=2)

    frameDecrypt.pack()



# Función para mostrar archivos en la nube
def show_cloud_files(frame):
    frame.destroy()
    frameCloud = Frame(root)
    
    # Listar archivos disponibles
    files = list_files()
    Label(frameCloud, text="Archivos disponibles en la nube:").grid(row=0, column=0, columnspan=2)
    
    for idx, file in enumerate(files):
        Label(frameCloud, text=file).grid(row=idx+1, column=0)
    
    # Botón para volver al login
    backButton = Button(frameCloud, text="Volver", command=lambda: generate_Login(frameCloud))
    backButton.grid(row=len(files)+1, column=0, columnspan=2)
    
    frameCloud.pack()

# Función para subir un archivo
def upload_document(frame):
    frame.destroy()
    frameUpload = Frame(root)

    Label(frameUpload, text="Ruta del archivo a subir:").grid(row=0, column=0)
    filePathEntry = Entry(frameUpload, width=30)
    filePathEntry.grid(row=0, column=1)

    def upload():
        file_path = filePathEntry.get()
        if os.path.exists(file_path):
            response = upload_file(file_path)
            messagebox.showinfo("Subida", response["message"])
            generate_Login(frameUpload)
        else:
            messagebox.showerror("Error", "El archivo no existe.")

    uploadButton = Button(frameUpload, text="Subir", command=upload)
    uploadButton.grid(row=1, column=0, columnspan=2)
    frameUpload.pack()

# Función para registrar un nuevo usuario
def register_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return {"success": True, "message": "Usuario registrado exitosamente."}
        except sqlite3.IntegrityError:
            return {"success": False, "message": "El nombre de usuario ya está registrado."}

# Función para verificar credenciales
def verify_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row and row[0] == password:
            return True
        return False

# Función para mostrar el registro
def generate_Register(frame):
    frame.destroy()
    frameRegister = Frame(root)
    
    Label(frameRegister, text="Registrar Nuevo Usuario").grid(row=0, column=0, columnspan=2)

    Label(frameRegister, text="Nombre de Usuario:").grid(row=1, column=0)
    usernameEntry = Entry(frameRegister)
    usernameEntry.grid(row=1, column=1)

    Label(frameRegister, text="Contraseña:").grid(row=2, column=0)
    passwordEntry = Entry(frameRegister, show="*")
    passwordEntry.grid(row=2, column=1)

    def register():
        username = usernameEntry.get().strip()
        password = passwordEntry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        response = register_user(username, password)
        if response["success"]:
            messagebox.showinfo("Registro", response["message"])
            generate_Login(frameRegister)
        else:
            messagebox.showerror("Error", response["message"])

    registerButton = Button(frameRegister, text="Registrar", command=register)
    registerButton.grid(row=3, column=0, columnspan=2)

    backButton = Button(frameRegister, text="Volver", command=lambda: generate_MainMenu(frameRegister))
    backButton.grid(row=4, column=0, columnspan=2)

    frameRegister.pack()

# Función de Login
def login(frame):
    username = txtUsername.get("1.0", "end").strip()
    password = txtPassword.get("1.0", "end").strip()
    
    if verify_user(username, password):
        messagebox.showinfo("Login", "Bienvenido, " + username)
        frame.destroy()
        frameMenu = Frame(root)

        # Opciones después del login
        Label(frameMenu, text="Opciones disponibles:").grid(row=0, column=0, columnspan=2)

        Button(frameMenu, text="Subir Archivo", command=lambda: upload_document(frameMenu)).grid(row=1, column=0, columnspan=2)
        Button(frameMenu, text="Ver Archivos en la Nube", command=lambda: show_cloud_files(frameMenu)).grid(row=2, column=0, columnspan=2)
        Button(frameMenu, text="Descifrar Archivo", command=lambda: decrypt_document(frameMenu)).grid(row=3, column=0, columnspan=2)

        frameMenu.pack()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")

# Generar interfaz de Login
def generate_Login(fram):
    global txtUsername, txtPassword
    frameL = Frame(root)
    fram.destroy()

    txtLabelUsername = Label(frameL, text="Ingresa un nombre de usuario:")
    txtUsername = Text(frameL, width=15, height=1)
    txtLabelPassword = Label(frameL, text="Ingresa una contraseña:")
    txtPassword = Text(frameL, width=15, height=1)

    LoginButton = Button(frameL, text="Login", command=lambda: login(frameL))

    txtLabelUsername.grid(row=0, column=0)
    txtUsername.grid(row=0, column=1)
    txtLabelPassword.grid(row=1, column=0)
    txtPassword.grid(row=1, column=1)

    LoginButton.grid(row=2, column=0, columnspan=2)

    backButton = Button(frameL, text="Volver", command=lambda: generate_MainMenu(frameL))
    backButton.grid(row=3, column=0, columnspan=2)

    frameL.pack()

# Generar menú principal (Inicio)
def generate_MainMenu(frame):
    frame.destroy()
    frameMain = Frame(root)
    
    Label(frameMain, text="Bienvenido al Sistema").grid(row=0, column=0, columnspan=2)

    Button(frameMain, text="Iniciar Sesión", command=lambda: generate_Login(frameMain)).grid(row=1, column=0, columnspan=2)
    Button(frameMain, text="Registrarse", command=lambda: generate_Register(frameMain)).grid(row=2, column=0, columnspan=2)

    frameMain.pack()

# Configuración inicial de la ventana
root = Tk()
root.title("Sistema de Deduplicación Segura")
generate_MainMenu(Frame(root))
root.mainloop()