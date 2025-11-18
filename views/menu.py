import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox
from datetime import datetime # Importar para formatear la fecha
from PIL import Image, ImageTk, ImageOps
from models.usuario import Usuario


from models.mascota import Mascota
from controllers.guardar_cargar import guardar_datos
# Asegúrate de que las rutas y nombres de archivo sean correctos
from views.ventana_turnos import ventana_sacar_turno, ventana_asistente_ia 
from utils.turno_utilis import obtener_y_ordenar_turnos 
from views.ventana_asistente_ia import ventana_asistente_ia

# --- Función para crear el submenú de Turnos ---
def crear_menu_turnos(parent_widget, usuario, lista_usuarios):
    """
    Crea y muestra un menú contextual para las opciones de turno.
    """
    menu = tk.Menu(parent_widget, tearoff=0)

    # Opción 1: Sacar Turno (Formulario Manual)
    menu.add_command(
        label="Sacar Turno (Manual)",
        command=lambda: ventana_sacar_turno(usuario, lista_usuarios)
    )

    # Opción 2: Asistente IA
    menu.add_command(
        label="🤖 Asistente IA",
        command=lambda: ventana_asistente_ia(usuario, lista_usuarios)
    )
    
    return menu

# --- Ventana principal del menú ---
def abrir_menu(usuario, lista_usuarios):
    ventana_menu = tk.Toplevel()
    ventana_menu.title(f"🐾 SystemPet | Menú Principal ({usuario.nombre.capitalize()})")
    ventana_menu.geometry("900x800") 
    ventana_menu.config(bg="#507383")
    
    # Pre-calculamos los turnos y el menú desplegable (siempre va antes de usarse)
    menu_turnos = crear_menu_turnos(ventana_menu, usuario, lista_usuarios)
    turnos_ordenados = obtener_y_ordenar_turnos(usuario)
    
    # ---------------------------------------------
    # 1. FRAME PRINCIPAL (Para contener el menú lateral y el contenido principal)
    # ---------------------------------------------
    main_frame = tk.Frame(ventana_menu, bg="#507383")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ---------------------------------------------
    # 2. FRAME IZQUIERDO: Contiene la Bienvenida y los Botones Justificados
    # ---------------------------------------------
    frame_menu_izquierdo = tk.Frame(main_frame, bg="#507383")
    # side="left" lo coloca a la izquierda; anchor="nw" lo alinea arriba y a la izquierda
    frame_menu_izquierdo.pack(side="left", anchor="center", padx=(10, 40))

    # Bienvenida personalizada (Centrada sobre los botones)
    lbl_bienvenida = tk.Label(
        frame_menu_izquierdo, # Empaquetado en el frame izquierdo
        text=f"Bienvenido/a, {usuario.nombre.capitalize()} 🐶",
        font=("cambria", 25, "bold"),
        bg="#507383",
    )
    lbl_bienvenida.pack(pady=15)
    
    
    # --- BOTONES JUSTIFICADOS A LA IZQUIERDA (pack con anchor="w") ---
    
    # Botón: Mis Mascotas (CORREGIDA la llamada a ver_mis_mascotas)
    tk.Button(
        frame_menu_izquierdo,
        text="🐕 Mis Mascotas",
        font=("Arial", 12, "bold"),
        bg="#FFF59D", width=25,
        command=lambda: ver_mis_mascotas(usuario, lista_usuarios) # CORREGIDO
    ).pack(pady=10, anchor="w") 

    # Botón: Registrar nueva mascota
    tk.Button(
        frame_menu_izquierdo,
        text="➕ Registrar Mascota",
        font=("Arial", 12, "bold"),
        bg="#AED581", width=25,
        command=lambda: ventana_registrar_mascota(usuario, lista_usuarios)
    ).pack(pady=10, anchor="w") 

    # Botón Principal de Turnos (SUBMENÚ DESPLEGABLE)
    def mostrar_menu(event):
        try:
            menu_turnos.tk_popup(event.x_root, event.y_root)
        finally:
            menu_turnos.grab_release()
            
    btn_turnos = tk.Button(
        frame_menu_izquierdo,
        text="📅 Turnos",
        font=("Arial", 12, "bold"),
        bg="#FFB74D", width=25,
    )
    btn_turnos.bind("<Button-1>", mostrar_menu)
    btn_turnos.pack(pady=10, anchor="w") 

    btn_asistente_ia = tk.Button(
    # Reemplaza 'nombre_del_frame_donde_van_los_botones' por el Frame correcto
    master=frame_menu_izquierdo, 
    text="Consulta Diagnóstico IA 🧠",
    font=("Arial", 12, "bold"),
    bg="#28a745", # Color verde para destacar
    fg="black",
    width=25,
    command=lambda: ventana_asistente_ia(usuario, lista_usuarios)
)
    btn_asistente_ia.pack(pady=25, anchor="w")
    
    # Botón: Ver estudios
    tk.Button(
        frame_menu_izquierdo,
        text="📋 Ver Estudios",
        font=("Arial", 12, "bold"),
        bg="#90CAF9", width=25
    ).pack(pady=10, anchor="w") 
    
    # Botón: Cerrar sesión
    tk.Button(
        frame_menu_izquierdo,
        text="🚪 Cerrar Sesión",
        font=("Arial", 12, "bold"),
        bg="#EF9A9A", width=25,
        command=ventana_menu.destroy
    ).pack(pady=25, anchor="w") 
    
    # ---------------------------------------------
    # 3. FRAME DERECHO: Próximos Turnos y Espacio para Imagen
    # ---------------------------------------------
    # side="left" después del frame izquierdo, fill="both" y expand=True para ocupar el resto del espacio
    frame_contenido_derecho = tk.Frame(main_frame, bg="#507383")
    frame_contenido_derecho.pack(side="left", fill="both", expand=True, padx=10, anchor="center")

    # ---------------------------------------------
    # A. TÍTULO PRÓXIMOS TURNOS (Centrado en este Frame)
    # ---------------------------------------------
    tk.Label(
        frame_contenido_derecho, 
        text="📅 Su próximo Turno...", 
        font=("cambria", 14, "bold"), 
        bg="#507383",
        anchor="center"
    ).pack(pady=(5, 5)) 

    # Contenedor para la lista de turnos
    frame_turnos = tk.Frame(frame_contenido_derecho, bd=2, relief=tk.SUNKEN, bg="white")
    frame_turnos.pack(pady=5, padx=(10, 40), fill="both",anchor="center")
    
    # --- CÓDIGO DE DIBUJO DE LOS TURNOS (CORREGIDO EL SYNTAX ERROR y el slice) ---
    if turnos_ordenados:
        for i, item in enumerate(turnos_ordenados[:1]): # Muestra le primer turno
            fecha_formateada = item["fecha_hora"].strftime("%a, %d %b | %H:%M hs")
            info_turno = ( 
                f"🐾 {item['mascota']}\n"
                f"🗓️ {fecha_formateada}\n"
                f"🧑‍⚕️ {item['info'].veterinario} - Motivo: {item['info'].motivo}"
            ) 
            
            lbl_turno = tk.Label(
                frame_turnos,
                text=info_turno,
                justify=tk.LEFT,
                anchor="w",
                bg="#E2E2E2" if i % 2 == 0 else "#E2E2E2", 
                font=("cambria", 12),
                padx=5, pady=5,
                bd=1, 
            )
            lbl_turno.pack(fill="x", pady=2)
            
        if len(turnos_ordenados) > 1:
             tk.Label(frame_turnos, text=f"...y {len(turnos_ordenados) - 1} turnos más", bg="white", font=("cambria", 9, "italic")).pack(pady=5)
             
    else:
        tk.Label(
            frame_turnos, 
            text="✅ No tienes próximos turnos agendados.", 
            font=("cambria", 12), 
            bg="#E2E2E2"
        ).pack(fill="x", pady=10)


 
    # B. IMAGEN (Cargar y mostrar)
    
    # 1. Definir la ruta de la imagen
    ruta_imagen = os.path.join(os.path.dirname(__file__), "imagen","image1.png")
    
    # Usaremos un bloque try/except por si el archivo de imagen no se encuentra
    try:
        # 2. Cargar la imagen usando PIL y redimensionar
        img_pil = Image.open(ruta_imagen).convert("RGBA")
        
        # Redimensiona la imagen a un tamaño adecuado para el espacio. 
       
        img_pil = img_pil.resize((350, 200), Image.LANCZOS)
        
        # 3. Convertir a PhotoImage para Tkinter
        logo_tk = ImageTk.PhotoImage(img_pil)
        
        # 4. Crear la etiqueta y mostrar la imagen
        lbl_imagen = tk.Label(frame_contenido_derecho, image=logo_tk, bg="#507383")
        
        # OBLIGATORIO: Guardar una referencia a la imagen para que Tkinter no la borre
        lbl_imagen.image = logo_tk
        
        lbl_imagen.pack(side="bottom",pady=20, padx=10, fill="both", expand=True)

    except FileNotFoundError:
        # Mensaje de respaldo si la imagen no se encuentra
        tk.Label(
            frame_contenido_derecho, 
            text="[Error: Imagen 'image1.png' no encontrada]", 
            font=("Arial", 10, "italic"), 
            bg="#507383", 
            height=10
        ).pack(pady=20, padx=10, fill="both", expand=True)
    
    ventana_menu.mainloop()

def ver_mis_mascotas(usuario, lista_usuarios):
    # Asegúrate de importar tkinter, messagebox, os, y de tener PIL (Image, ImageTk) accesible.

    ventana_lista = tk.Toplevel()
    ventana_lista.title("🐾 Mis Mascotas")
    ventana_lista.geometry("1000x550")
    ventana_lista.config(bg="#507383")

    # FRAME PRINCIPAL (divide izquierda lista | derecha imagen)
    main_pet_frame = tk.Frame(ventana_lista, bg="#507383")
    main_pet_frame.pack(fill="both", expand=True)

    # -----------------------------------------------------------------
    # ----- FRAME IZQUIERDO: TÍTULO + LISTA CON SCROLL + CERRAR -----
    # -----------------------------------------------------------------
    frame_scroll_contenedor = tk.Frame(main_pet_frame, bg="#507383")
    frame_scroll_contenedor.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    
    # 📌 TÍTULO (Ahora en el lado IZQUIERDO)
    tk.Label(
        frame_scroll_contenedor,
        text=f"Mascotas de {usuario.nombre.capitalize()}🐶",
        font=("cambria", 25, "bold"),
        bg="#507383" # Color de fondo del contenedor
    ).pack(pady=10)


    if not usuario.mascotas:
        tk.Label(
            frame_scroll_contenedor,
            text="No hay mascotas registradas 😿",
            font=("Arial", 13, "italic"),
            bg="#B3E5FC"
        ).pack(pady=20)
        
        # BOTÓN CERRAR (Se mantiene en este frame)
        tk.Button(
            frame_scroll_contenedor,
            text="Cerrar",
            bg="#C8F0F5",
            font=("Arial", 11, "bold"),

            command=ventana_lista.destroy
        ).pack(side="bottom", pady=20, fill="x", padx=30)
        return

    """# CANVAS + SCROLLBAR (VERTICAL)
    canvas = tk.Canvas(frame_scroll_contenedor, bg="#B3E5FC", highlightthickness=0)
    scrollbar_y = tk.Scrollbar(frame_scroll_contenedor, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_y.pack(side="right", fill="y")
    # Nota: El canvas ya ocupa el espacio disponible a la izquierda del scrollbar
    canvas.pack(side="top", fill="both", expand=True, padx=(0, 10)) 

    # Frame scrollable
    scrollable_frame = tk.Frame(canvas, bg="#E1F5FE")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
"""
    # ----- LISTA DE MASCOTAS (Dentro de scrollable_frame) -----
    for mascota in usuario.mascotas:
        
        frame_mascota = tk.Frame(
            frame_scroll_contenedor, #scroll
            bg="#93B2CC",
            bd=2,
            relief="raised",
            padx=10,
            pady=10
        )
        frame_mascota.pack(fill="x", padx=15, pady=10)

        bg_color = "#93B2CC"

        # ---- TÍTULO ----
        tk.Label(
            frame_mascota,
            text=f"🐶 {mascota.nombre.capitalize()}",
            font=("Arial", 13, "bold"),
            bg=bg_color
        ).grid(row=0, column=0, columnspan=2, pady=5, sticky="w")


        # ---- DATOS ----
        tk.Label(frame_mascota, text=f"📅 Nacimiento: {mascota.fecha_nac}", bg=bg_color).grid(row=1, column=0, sticky="w")
        tk.Label(frame_mascota, text=f"🧬 Raza: {mascota.raza.capitalize()}", bg=bg_color).grid(row=2, column=0, sticky="w")
        tk.Label(frame_mascota, text=f"⚧ Sexo: {mascota.sexo.capitalize()}", bg=bg_color).grid(row=3, column=0, sticky="w")
        tk.Label(frame_mascota, text=f"⚖️ Peso: {mascota.peso} kg", bg=bg_color).grid(row=4, column=0, sticky="w")
        tk.Label(frame_mascota, text=f"💉 Vacunas: {mascota.vacunas.capitalize()}", bg=bg_color, wraplength=250).grid(row=5, column=0, sticky="w")


        # ---- TURNOS ----
        frame_turnos = tk.Frame(frame_mascota, bg=bg_color)
        frame_turnos.grid(row=1, column=1, rowspan=5, sticky="ne", padx=10)

        if mascota.turnos:
            tk.Label(frame_turnos, text="📅 Turnos:", bg=bg_color, font=("Arial", 11, "bold")).pack(anchor="w")
            for t in mascota.turnos[:3]:
                tk.Label(
                    frame_turnos,
                    text=f"🕐 {t.fecha} {t.hora} - {t.motivo}",
                    bg=bg_color,
                    wraplength=300,
                    justify="left"
                ).pack(anchor="w")
        else:
            tk.Label(frame_turnos, text="❌ Sin turnos", bg=bg_color).pack(anchor="w")


        # =====================================================
        # 📌 BOTONES EDITAR Y ELIMINAR (Mantenemos las funciones internas)
        # =====================================================

        def editar_mascota_actual(m=mascota):
            # Asumiendo que las funciones guardar_datos y messagebox están importadas/accesibles
            
            ventana_edit = tk.Toplevel()
            ventana_edit.title(f"Editar {m.nombre}")
            ventana_edit.geometry("350x400")
            ventana_edit.config(bg="#E3F2FD")
            
            tk.Label(ventana_edit, text="Editar Mascota", bg="#E3F2FD",
                     font=("Arial", 14, "bold")).pack(pady=10)

            campos = {}

            for label_text, valor_inicial in [
                ("Nombre", m.nombre),
                ("Fecha de Nac.", m.fecha_nac),
                ("Raza", m.raza),
                ("Sexo", m.sexo),
                ("Peso", m.peso),
                ("Vacunas", m.vacunas)
            ]:
                tk.Label(ventana_edit, text=label_text, bg="#E3F2FD").pack()
                entry = tk.Entry(ventana_edit)
                entry.pack()
                entry.insert(0, valor_inicial)
                campos[label_text] = entry

            def guardar_cambios():
                # Lógica de guardar cambios, asumiendo que 'guardar_datos' existe
                m.nombre = campos["Nombre"].get()
                m.fecha_nac = campos["Fecha de Nac."].get()
                m.raza = campos["Raza"].get()
                m.sexo = campos["Sexo"].get()
                m.peso = campos["Peso"].get()
                m.vacunas = campos["Vacunas"].get()
                
                # guardar_datos(lista_usuarios) # Descomentar cuando la función esté disponible
                messagebox.showinfo("Guardado", "Mascota actualizada correctamente.")
                ventana_edit.destroy()

            tk.Button(ventana_edit, text="Guardar Cambios",
                      bg="#C5E1A5", command=guardar_cambios).pack(pady=10)

            tk.Button(ventana_edit, text="Cancelar",
                      bg="#EF9A9A", command=ventana_edit.destroy).pack()

        # ----------------------------------------------------------------------

        def eliminar_mascota_actual(m=mascota):
            # Lógica para eliminar la mascota, asumiendo que 'guardar_datos' y 'messagebox' existen
            confirmar = messagebox.askyesno(
                "Eliminar Mascota",
                f"¿Seguro que deseas eliminar a {m.nombre}?"
            )
            if confirmar:
                usuario.mascotas.remove(m)
                # guardar_datos(lista_usuarios) # Descomentar cuando la función esté disponible
                messagebox.showinfo("Eliminada", "Mascota eliminada correctamente.")
                ventana_lista.destroy()
                # Recargar la ventana de la lista para ver el cambio
                # ver_mis_mascotas(usuario, lista_usuarios)


        # ---- BOTONES ----
        botones_frame = tk.Frame(frame_mascota, bg=bg_color)
        botones_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(botones_frame, text="✏ Editar",font=("arial",11,"bold"),
                  bg="#FFF59D", width=10,
                  command=editar_mascota_actual).pack(side="left", padx=5)

        tk.Button(botones_frame, text="🗑 Eliminar",
                  bg="#C4B5B5", width=10,
                  command=eliminar_mascota_actual).pack(side="left", padx=5)

    # 📌 BOTÓN CERRAR (FUERA DEL CANVAS, ABAJO DE LA LISTA)
    # Lo colocamos aquí para que esté siempre visible aunque la lista tenga scroll
    tk.Button(
        frame_scroll_contenedor,
        text="Cerrar",
        bg="#C8F0F5",
        font=("Arial", 11, "bold"),
        command=ventana_lista.destroy
    ).pack(pady=10)

    # -----------------------------------------------------------------
    # ----- FRAME DERECHO: IMAGEN ESTÁTICA -----
    # -----------------------------------------------------------------
    frame_imagen_mascotas = tk.Frame(main_pet_frame, bg="#507383", width=300) 
    frame_imagen_mascotas.pack(side="right", fill="both", padx=15, pady=15)
    frame_imagen_mascotas.pack_propagate(False)

    # IMAGEN (Lógica de carga de imagen, se mantiene)
    ruta_imagen = os.path.join(os.path.dirname(__file__), "imagen", "image2.png")

    try:
        from PIL import Image, ImageTk
        img_pil = Image.open(ruta_imagen).convert("RGBA")
        img_pil.thumbnail((250, 250), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(img_pil)

        lbl_imagen = tk.Label(frame_imagen_mascotas, image=logo_tk, bg="#507383")
        lbl_imagen.image = logo_tk
        lbl_imagen.pack(expand=True, padx=10, pady=10)
    except Exception:
        tk.Label(
            frame_imagen_mascotas,
            text="[Imagen no disponible]",
            bg="#D4E6F1",
            font=("Arial", 10, "italic")
        ).pack(expand=True, padx=10, pady=10)
####
# --- Ventana para registrar mascota ---
def ventana_registrar_mascota(usuario, lista_usuarios):
    ventana_mascota = tk.Toplevel()
    ventana_mascota.title("Registrar Mascota 🐾")
    ventana_mascota.geometry("400x400")
    ventana_mascota.config(bg="#B3E5FC")

    tk.Label(ventana_mascota, text="Nombre:", bg="#B3E5FC").pack(pady=3)
    entry_nombre = tk.Entry(ventana_mascota)
    entry_nombre.pack()

    tk.Label(ventana_mascota, text="Fecha de Nacimiento (DD/MM/AAAA):", bg="#B3E5FC").pack(pady=3)
    entry_fecha = tk.Entry(ventana_mascota)
    entry_fecha.pack()

    tk.Label(ventana_mascota, text="Raza:", bg="#B3E5FC").pack(pady=3)
    entry_raza = tk.Entry(ventana_mascota)
    entry_raza.pack()

    tk.Label(ventana_mascota, text="Sexo:", bg="#B3E5FC").pack(pady=3)
    entry_sexo = tk.Entry(ventana_mascota)
    entry_sexo.pack()

    tk.Label(ventana_mascota, text="Peso (kg):", bg="#B3E5FC").pack(pady=3)
    entry_peso = tk.Entry(ventana_mascota)
    entry_peso.pack()

    tk.Label(ventana_mascota, text="Vacunas (separadas por coma):", bg="#B3E5FC").pack(pady=3)
    entry_vacunas = tk.Entry(ventana_mascota)
    entry_vacunas.pack()

    def guardar_mascota():
        nombre = entry_nombre.get().strip()
        fecha_nac = entry_fecha.get().strip()
        raza = entry_raza.get().strip()
        sexo = entry_sexo.get().strip()
        peso = entry_peso.get().strip()
        vacunas = entry_vacunas.get().strip()

        # Verificar si la mascota ya está registrada (por nombre)
        for m in usuario.mascotas:
            if m.nombre.lower() == nombre.lower():
                messagebox.showerror("Error", f"La mascota '{nombre}' ya está registrada 🐶")
                return

        if not nombre or not fecha_nac or not raza:
            messagebox.showerror("Error", "Por favor complete todos los campos obligatorios.")
            return

        nueva = Mascota(nombre, fecha_nac, raza, sexo, peso, vacunas)
        usuario.agregar_mascota(nueva)
        guardar_datos(lista_usuarios)

        messagebox.showinfo("Éxito", f"Mascota '{nombre}' registrada correctamente 🐕")
        ventana_mascota.destroy()

    tk.Button(
        ventana_mascota, text="Guardar Mascota",
        bg="#C5E1A5", font=("Arial", 11, "bold"),
        command=guardar_mascota
    ).pack(pady=15)

    tk.Button(
        ventana_mascota, text="Cancelar",
        bg="#EF9A9A", font=("Arial", 11, "bold"),
        command=ventana_mascota.destroy
    ).pack(pady=5)