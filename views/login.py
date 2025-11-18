import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from controllers.guardar_cargar import guardar_datos, cargar_datos
from models.usuario import Usuario
from views.menu import abrir_menu


def iniciar_login():  # 👈 Esta función es llamada desde main.py
    usuarios = cargar_datos()

    def verificar_login():
        dni = entry_dni.get().strip()
        if not dni.isdigit():
            messagebox.showerror("Error", "El DNI debe ser numérico")
            return

        usuario_encontrado = next((u for u in usuarios if str(u.dni) == dni), None)
        if usuario_encontrado:
            root.destroy()
            abrir_menu(usuario_encontrado, usuarios)
        else:
            messagebox.showerror("Acceso denegado", "Usuario no encontrado")

    def crear_usuario_ui():
        ventana = tk.Toplevel(root)
        ventana.title("Crear usuario 🧍‍♀️🐾")
        ventana.geometry("400x450")
        ventana.config(bg="#507383")

        frame_ventana_usuario = tk.Frame(ventana, bg="#507383", width=500) 
        frame_ventana_usuario.pack(side="left", fill="both", padx=15, pady=15)

        lbl_nuevo_usuario = tk.Label(
        frame_ventana_usuario, # Empaquetado en el frame izquierdo
        text=f"Cree su usuario 🐶",
        font=("cambria", 25, "bold"),
        bg="#507383",
        )
        lbl_nuevo_usuario.pack(pady=15)

        tk.Label(frame_ventana_usuario, text="Nombre completo:", bg="#507383").pack(pady=5)
        entry_nombre = tk.Entry(frame_ventana_usuario)
        entry_nombre.pack()

        tk.Label(frame_ventana_usuario, text="Fecha de nacimiento (DD/MM/AAAA):", bg="#507383").pack(pady=5)
        entry_fecha = tk.Entry(frame_ventana_usuario)
        entry_fecha.pack()

        tk.Label(frame_ventana_usuario, text="DNI:", bg="#507383").pack(pady=5)
        entry_dni_nuevo = tk.Entry(frame_ventana_usuario)
        entry_dni_nuevo.pack()

        tk.Label(frame_ventana_usuario, text="Email:", bg="#507383").pack(pady=5)
        entry_email = tk.Entry(frame_ventana_usuario)
        entry_email.pack()

        tk.Label(frame_ventana_usuario, text="Teléfono:", bg="#507383").pack(pady=5)
        entry_tel = tk.Entry(frame_ventana_usuario)
        entry_tel.pack()

        def guardar_usuario():
            nombre = entry_nombre.get().strip()
            fecha = entry_fecha.get().strip()
            dni_nuevo = entry_dni_nuevo.get().strip()
            email = entry_email.get().strip()
            tel = entry_tel.get().strip()

            if not all([nombre, fecha, dni_nuevo, email, tel]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            if any(str(u.dni) == dni_nuevo for u in usuarios):
                messagebox.showerror("Error", "Ya existe un usuario con ese DNI.")
                return

            nuevo_usuario = Usuario(nombre, fecha, dni_nuevo, email, tel)
            usuarios.append(nuevo_usuario)
            guardar_datos(usuarios)

            messagebox.showinfo("Éxito", f"Usuario {nombre} creado correctamente 🐾")
            ventana.destroy()

        tk.Button(
            frame_ventana_usuario, text="Guardar usuario", bg="#B3E5FC", fg="grey",
            font=("Aptos", 11, "bold"), relief="raised",
            command=guardar_usuario
        ).pack(pady=20)

    # --- Ventana principal de login ---
    root = tk.Tk()
    root.title("🐾 SystemPet | Login")
    root.geometry("400x500")
    root.config(bg="#507383")

    frame = tk.Frame(root, bg="#507383")
    frame.pack(expand=True)

    ruta_logo = os.path.join(os.path.dirname(__file__), "imagen", "logo1.png")
    try:
        logo_img = Image.open(ruta_logo).convert("RGBA")
        logo_img = logo_img.resize((380, 380), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        lbl_logo = tk.Label(frame, image=logo_tk, bg="#507383")
        lbl_logo.image = logo_tk
        lbl_logo.pack(pady=(0, 0))
    except:
        tk.Label(frame, text="🐾 SystemPet 🐾", bg="#507383",
                 font=("Aptos Black", 18, "bold")).pack(pady=10)

    tk.Label(frame, text="Ingrese su DNI:", bg="#507383",
             font=("Aptos", 14, "bold")).pack(pady=(2, 0))
    entry_dni = tk.Entry(frame, font=("cambria", 12), width=20)
    entry_dni.pack(pady=5)

    tk.Button(frame, text="Ingresar", bg="#D6DBDB", fg="black",
              font=("Aptos Bold", 11, "bold"), relief="raised",
              command=verificar_login).pack(pady=5)

    tk.Button(frame, text="Crear usuario", bg="#D6DBDB", fg="black",
              font=("Aptos", 11, "bold"), relief="raised",
              command=crear_usuario_ui).pack(pady=5)

    root.mainloop()
