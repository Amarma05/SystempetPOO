import tkinter as tk
from tkinter import messagebox, ttk
from models.turno import Turno
from controllers.guardar_cargar import guardar_datos
from models.moduloIA import Prediccion_turnos, PROFESIONALES

# Función principal para la ventana de turnos
def ventana_sacar_turno(usuario, lista_usuarios):
    if not usuario.mascotas:
        messagebox.showwarning("Advertencia", "Necesitas registrar una mascota antes de sacar un turno.")
        return

    ventana_turno = tk.Toplevel()
    ventana_turno.title("📅 Sacar Turno Veterinario")
    ventana_turno.geometry("400x500")
    ventana_turno.config(bg="#B3E5FC")

    # --- Frame principal ---
    frame = tk.Frame(ventana_turno, bg="#B3E5FC", padx=20, pady=20)
    frame.pack(expand=True)

    # 1. Selección de Mascota
    tk.Label(frame, text="1. Selecciona tu Mascota:", bg="#B3E5FC", font=("Arial", 11, "bold")).pack(pady=(0, 5))
    
    # Crea una lista de nombres de mascotas para el Combobox
    nombres_mascotas = [m.nombre for m in usuario.mascotas]
    
    combo_mascotas = ttk.Combobox(frame, values=nombres_mascotas, state="readonly", width=30)
    combo_mascotas.set(nombres_mascotas[0]) # Selecciona la primera por defecto
    combo_mascotas.pack(pady=5)
    
    # 2. Fecha y Hora (Aquí usarás DatePicker si lo instalas, por ahora solo Entry)
    tk.Label(frame, text="2. Fecha del Turno (DD/MM/AAAA):", bg="#B3E5FC").pack(pady=(15, 5))
    entry_fecha = tk.Entry(frame, width=30)
    entry_fecha.pack(pady=5)

    tk.Label(frame, text="3. Hora del Turno (HH:MM):", bg="#B3E5FC").pack(pady=(15, 5))
    entry_hora = tk.Entry(frame, width=30)
    entry_hora.pack(pady=5)
    
    # 3. Motivo de la Consulta
    tk.Label(frame, text="4. Motivo de la Consulta:", bg="#B3E5FC").pack(pady=(15, 5))
    entry_motivo = tk.Entry(frame, width=30)
    entry_motivo.pack(pady=5)
    
    # 4. Veterinario (Opcional)
    tk.Label(frame, text="5. Veterinario (Opcional - Escriba el nombre):", bg="#B3E5FC").pack(pady=(15, 5))
    entry_veterinario = tk.Entry(frame, width=30)
    entry_veterinario.pack(pady=5)

    # --- Función para guardar el turno ---
    def guardar_turno():
        nombre_mascota = combo_mascotas.get()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        motivo = entry_motivo.get().strip()
        veterinario = entry_veterinario.get().strip() or "General" # Si está vacío, es "General"

        if not all([nombre_mascota, fecha, hora, motivo]):
            messagebox.showerror("Error", "Los campos Mascota, Fecha, Hora y Motivo son obligatorios.")
            return

        # 1. Crear el objeto Turno
        nuevo_turno = Turno(fecha, hora, motivo, veterinario)
        
        # 2. Buscar la mascota y agregarle el turno
        mascota_encontrada = next((m for m in usuario.mascotas if m.nombre == nombre_mascota), None)

        if mascota_encontrada:
            mascota_encontrada.agregar_turno(nuevo_turno)
            
            # 3. Guardar los datos de todos los usuarios
            guardar_datos(lista_usuarios) 
            
            messagebox.showinfo("Éxito", f"Turno agendado para {nombre_mascota} el {fecha} a las {hora}.")
            ventana_turno.destroy()
        else:
            messagebox.showerror("Error Interno", "No se pudo encontrar la mascota seleccionada.")


    # Botón de Guardar
    tk.Button(
        frame, text="Agendar Turno",
        bg="#FFC107", font=("Arial", 12, "bold"),
        command=guardar_turno
    ).pack(pady=20)

def ventana_asistente_ia(usuario, lista_usuarios):
    if not usuario.mascotas:
        messagebox.showwarning("Advertencia", "Necesitas registrar una mascota antes de usar el Asistente IA.")
        return

    ventana_ia = tk.Toplevel()
    ventana_ia.title("🤖 Asistente IA Petly")
    ventana_ia.geometry("450x550")
    ventana_ia.config(bg="#E1BEE7")

    # --- Variables de control ---
    turno_recomendado = None
    
    # --- Frame Principal ---
    frame = tk.Frame(ventana_ia, bg="#E1BEE7", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Hola, soy Petly, tu Asistente IA 🤖", bg="#E1BEE7", font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(frame, text="Especifica tus preferencias de turno:", bg="#E1BEE7").pack(pady=5)
    
    # --- 1. Selección de Mascota ---
    tk.Label(frame, text="Mascota:", bg="#E1BEE7").pack(pady=(10, 0))
    nombres_mascotas = [m.nombre for m in usuario.mascotas]
    combo_mascotas = ttk.Combobox(frame, values=nombres_mascotas, state="readonly", width=30)
    combo_mascotas.set(nombres_mascotas[0])
    combo_mascotas.pack(pady=5)

    # --- 2. Preferencia de Horario (Mañana/Tarde) ---
    tk.Label(frame, text="Rango Horario de Preferencia:", bg="#E1BEE7").pack(pady=(10, 0))
    combo_horario = ttk.Combobox(frame, values=["mañana", "tarde-noche", "sin preferencia"], state="readonly", width=30)
    combo_horario.set("sin preferencia")
    combo_horario.pack(pady=5)

    # --- 3. Preferencia de Profesional ---
    tk.Label(frame, text="Profesional (Opcional):", bg="#E1BEE7").pack(pady=(10, 0))
    profesionales_lista = PROFESIONALES + ["sin preferencia"]
    combo_profesional = ttk.Combobox(frame, values=profesionales_lista, width=30)
    combo_profesional.set("sin preferencia")
    combo_profesional.pack(pady=5)

    # --- Área de Recomendación ---
    tk.Label(frame, text="Encontré esto para ti:", bg="#E1BEE7", font=("Arial", 12, "italic")).pack(pady=(20, 5))
    lbl_recomendacion = tk.Label(frame, text="Pulsa Buscar para ver la recomendación...", bg="#F3E5F5", wraplength=350, justify="left", bd=2, relief="groove")
    lbl_recomendacion.pack(fill="x", pady=10, ipady=10)
    
    # Botónes de Guardar y Buscar
    btn_guardar = tk.Button(frame, text="Guardar Turno Recomendado", bg="#C5E1A5", font=("Arial", 11, "bold"), state="disabled")
    btn_guardar.pack(pady=(20, 5))
    
    # --- Lógica de Búsqueda y Guardado ---
    
    def buscar_recomendacion():
        nonlocal turno_recomendado
        
        pref_hora = combo_horario.get()
        pref_prof = combo_profesional.get()
        
        # Llamar al módulo IA
        turno_recomendado = Prediccion_turnos(pref_hora, pref_prof)
        
        # Mostrar la recomendación
        texto = (
            f"✅ Fecha: {turno_recomendado.fecha}\n"
            f"✅ Hora: {turno_recomendado.hora}\n"
            f"✅ Profesional: {turno_recomendado.veterinario}\n"
            f"Motivo: {turno_recomendado.motivo}"
        )
        lbl_recomendacion.config(text=texto, bg="#E6EE9C")
        btn_guardar.config(state="normal", command=guardar_turno_recomendado)

    def guardar_turno_recomendado():
        nonlocal turno_recomendado
        nombre_mascota = combo_mascotas.get()
        
        if turno_recomendado is None:
            messagebox.showerror("Error", "No hay un turno para guardar.")
            return

        # 1. Buscar la mascota y agregarle el turno
        mascota_encontrada = next((m for m in usuario.mascotas if m.nombre == nombre_mascota), None)

        if mascota_encontrada:
            mascota_encontrada.agregar_turno(turno_recomendado)
            
            # 2. Guardar los datos de todos los usuarios
            guardar_datos(lista_usuarios) 
            
            messagebox.showinfo("Éxito", f"Turno recomendado agendado para {nombre_mascota}.")
            ventana_ia.destroy()
        else:
            messagebox.showerror("Error Interno", "No se pudo encontrar la mascota seleccionada.")


    # Botón de Búsqueda
    tk.Button(
        frame, text="Buscar Disponibilidad",
        bg="#FFB74D", font=("Arial", 11, "bold"),
        command=buscar_recomendacion
    ).pack(pady=5)
    
    tk.Button(frame, text="Cancelar", bg="#EF9A9A", command=ventana_ia.destroy).pack(pady=5)