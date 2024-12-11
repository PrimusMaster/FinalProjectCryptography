import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

def login_action():
    username = username_entry.get()
    password = password_entry.get()

    if username == "root" and password == "root":
        showinfo("Login exitoso", "Bienvenido, Admin!")
    else:
        showinfo("Error", "Usuario o contrase\u00f1a incorrectos")

# Crear main window
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x500")
root.resizable(False, False)
root.configure(bg="#f4f4f9")

# Create frame
frame = ttk.Frame(root, padding=45, style="Card.TFrame")
frame.pack(expand=True)

# Tittle
title_label = ttk.Label(frame, text="Iniciar Sesión", font=("Helvetica", 18), anchor="center", style="Title.TLabel")
title_label.pack(pady=10)

# Espacio para imagen
try:
    image = Image.open("../../src/login.png").convert("RGBA")
    # Procesar fondo transparente
    datas = image.getdata()
    new_data = []
    for item in datas:
        # Cambiar píxeles blancos a transparentes
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    image = image.resize((100, 100), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = ttk.Label(frame, image=photo)
    image_label.image = photo
    image_label.pack(pady=10)
except Exception as e:
    error_label = ttk.Label(frame, text="[Imagen no disponible]", font=("Helvetica", 10), style="Label.TLabel")
    error_label.pack(pady=10)


# User field
username_label = ttk.Label(frame, text="Usuario:", font=("Helvetica", 12), style="Label.TLabel")
username_label.pack(anchor="w", pady=(10, 0))
username_entry = ttk.Entry(frame, font=("Helvetica", 12))
username_entry.pack(fill="x", pady=5)

#password field
password_label = ttk.Label(frame, text="Contraseña:", font=("Helvetica", 12), style="Label.TLabel")
password_label.pack(anchor="w", pady=(10, 0))
password_entry = ttk.Entry(frame, show="*", font=("Helvetica", 12))
password_entry.pack(fill="x", pady=5)

# button login
login_button = ttk.Button(frame, text="Iniciar Sesión", command=login_action, style="Accent.TButton")
login_button.pack(pady=20)

#styles
style = ttk.Style()
style.configure("Card.TFrame", background="#88d9ff", relief="raised")
style.configure("Title.TLabel", background="#88d9ff", foreground="black", font=("Helvetica", 16, "bold"))
style.configure("Label.TLabel", background="#88d9ff", foreground="black")
style.configure("Accent.TButton", font=("Helvetica", 12), foreground="black", background="black")
style.map("Accent.TButton", background=[("active", "#1e84b4")])

# Ejecutar la aplicación
root.mainloop()
