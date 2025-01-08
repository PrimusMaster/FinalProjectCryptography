import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from modules.users.engine import *

user = User()

def user_interface(parent):
    def add_user():
        name = name_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        area = area_entry.get()
        age = int(age_entry.get())
        user.create_user(name, password, email, area, age)
        status_label.config(text="Usuario añadido correctamente.")

    def update_user():
        id = id_entry.get()
        field = field_entry.get()
        value = value_entry.get()
        fields_to_update = {field: value}
        user.update_user(id, **fields_to_update)
        status_label.config(text="Usuario actualizado correctamente.")

    def delete_user():
        id = id_entry.get()
        user.delete_user(id)
        status_label.config(text="Usuario eliminado correctamente.")

    def view_users():
        users = user.view_users()
        users_text.delete(1.0, tk.END)
        for u in users:
            users_text.insert(tk.END,
                              f"ID: {u.id}, Nombre: {u.name}, Correo: {u.mail}, Área: {u.area}, Edad: {u.age}\n")

    # Frame principal
    frame = ttk.Frame(parent, padding=10)
    frame.pack(fill="both", expand=True)

    # Título
    title_label = ttk.Label(frame, text="Gestión de Usuarios", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Campos para entrada de datos
    name_label = ttk.Label(frame, text="Nombre:")
    name_label.pack(anchor="w")
    name_entry = ttk.Entry(frame)
    name_entry.pack(fill="x", pady=5)

    password_label = ttk.Label(frame, text="Contraseña:")
    password_label.pack(anchor="w")
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack(fill="x", pady=5)

    email_label = ttk.Label(frame, text="Correo Electrónico:")
    email_label.pack(anchor="w")
    email_entry = ttk.Entry(frame)
    email_entry.pack(fill="x", pady=5)

    area_label = ttk.Label(frame, text="Área:")
    area_label.pack(anchor="w")
    area_entry = ttk.Entry(frame)
    area_entry.pack(fill="x", pady=5)

    age_label = ttk.Label(frame, text="Edad:")
    age_label.pack(anchor="w")
    age_entry = ttk.Entry(frame)
    age_entry.pack(fill="x", pady=5)

    id_label = ttk.Label(frame, text="ID del Usuario:")
    id_label.pack(anchor="w")
    id_entry = ttk.Entry(frame)
    id_entry.pack(fill="x", pady=5)

    field_label = ttk.Label(frame, text="Campo a Actualizar:")
    field_label.pack(anchor="w")
    field_entry = ttk.Entry(frame)
    field_entry.pack(fill="x", pady=5)

    value_label = ttk.Label(frame, text="Nuevo Valor del Campo:")
    value_label.pack(anchor="w")
    value_entry = ttk.Entry(frame)
    value_entry.pack(fill="x", pady=5)

    # Botones para las operaciones
    add_button = ttk.Button(frame, text="Añadir Usuario", command=add_user)
    add_button.pack(pady=5)

    update_button = ttk.Button(frame, text="Actualizar Usuario", command=update_user)
    update_button.pack(pady=5)

    delete_button = ttk.Button(frame, text="Eliminar Usuario", command=delete_user)
    delete_button.pack(pady=5)

    view_button = ttk.Button(frame, text="Ver Usuarios", command=view_users)
    view_button.pack(pady=5)

    # Area de visualización de usuarios
    users_text = tk.Text(frame, height=10)
    users_text.pack(fill="x", pady=10)

    # Etiqueta de estado
    status_label = ttk.Label(frame, text="", foreground="green")
    status_label.pack()

# Crear ventana secundaria
def create_window():
    new_window = tk.Toplevel(root)
    new_window.title("Gestión de Usuarios")
    new_window.geometry("400x900")
    user_interface(new_window)

def login_action():
    username = username_entry.get()
    password = password_entry.get()

    if username == "root" and password == "root":
        showinfo("Login exitoso", "Bienvenido, Admin!")
        create_window()  # Abrir la ventana de gestión de usuarios
    elif user.validate_user(username, password):
        showinfo("Login exitoso", f"Bienvenido, {user.name}!")
        create_window()  # Abrir la ventana de gestión de usuarios
    else:
        showinfo("Error", "Usuario o contraseña incorrectos")

# Ventana principal
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x500")
root.resizable(False, False)
root.configure(bg="#f4f4f9")

# Frame principal
frame = ttk.Frame(root, padding=45, style="Card.TFrame")
frame.pack(expand=True)

# Título
title_label = ttk.Label(frame, text="Iniciar Sesión", font=("Helvetica", 18), anchor="center", style="Title.TLabel")
title_label.pack(pady=10)

# Espacio para imagen
try:
    image = Image.open("../../src/login.png").convert("RGBA")
    image = image.resize((100, 100), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = ttk.Label(frame, image=photo)
    image_label.image = photo
    image_label.pack(pady=10)
except Exception:
    error_label = ttk.Label(frame, text="[Imagen no disponible]", font=("Helvetica", 10), style="Label.TLabel")
    error_label.pack(pady=10)

# Campos de usuario y contraseña
username_label = ttk.Label(frame, text="Usuario:", font=("Helvetica", 12), style="Label.TLabel")
username_label.pack(anchor="w", pady=(10, 0))
username_entry = ttk.Entry(frame, font=("Helvetica", 12))
username_entry.pack(fill="x", pady=5)

password_label = ttk.Label(frame, text="Contraseña:", font=("Helvetica", 12), style="Label.TLabel")
password_label.pack(anchor="w", pady=(10, 0))
password_entry = ttk.Entry(frame, show="*", font=("Helvetica", 12))
password_entry.pack(fill="x", pady=5)

# Botón de inicio de sesión
login_button = ttk.Button(frame, text="Iniciar Sesión", command=login_action, style="Accent.TButton")
login_button.pack(pady=20)

# Estilos
style = ttk.Style()
style.configure("Card.TFrame", background="#88d9ff", relief="raised")
style.configure("Title.TLabel", background="#88d9ff", foreground="black", font=("Helvetica", 16, "bold"))
style.configure("Label.TLabel", background="#88d9ff", foreground="black")
style.configure("Accent.TButton", font=("Helvetica", 12), foreground="black", background="black")
style.map("Accent.TButton", background=[("active", "#1e84b4")])

# Ejecutar la aplicación
root.mainloop()
