import os,sys
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox
import joblib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image, ImageTk, ImageOps
# Asegúrate de tener estas funciones disponibles o importadas si están en otro archivo
# from tu_archivo_utilidades import limpiar_texto 

# --- RECREACIÓN DE LAS FUNCIONES DE LIMPIEZA DE NLTK ---
# El modelo fue entrenado con estos pasos de limpieza, son CRUCIALES para la predicción
try:
    # Usamos try/except por si NLTK no está disponible o no se han descargado los recursos
    stop_words = set(stopwords.words('english'))
except Exception:
    # Fallback, si no se puede cargar, asumimos que no hay stopwords
    stop_words = set() 

def limpiar_texto(texto):
    """Aplica la misma limpieza que se usó en el entrenamiento del modelo."""
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    # Eliminar puntuación, comas, etc.
    texto = re.sub(r'[^a-z\s]', '', texto) 
    
    if stop_words:
        tokens = word_tokenize(texto)
        tokens_limpios = [w for w in tokens if w not in stop_words and len(w) > 2]
    else:
        # Si NLTK falla, al menos limpiamos y tokenizamos por espacio
        tokens_limpios = [w for w in texto.split() if len(w) > 2] 
        
    return " ".join(tokens_limpios)

# 📌 DICCIONARIO DE TRADUCCIÓN (Añade más si es necesario)
TRADUCCIONES_ENFERMEDADES = {
    'Rabies': 'Rabia',
    'Canine Parvovirus': 'Parvovirus Canino',
    'Canine Distemper': 'Moquillo Canino',
    'Bovine Tuberculosis': 'Tuberculosis Bovina',
    'Foot and Mouth Disease': 'Fiebre Aftosa (FMD)',
    'Brucellosis': 'Brucelosis',
    'Influenza': 'Gripe/Influenza',
    'Anthrax': 'Ántrax (Carbunco)',
    # Agrega más enfermedades que pueda predecir tu modelo aquí
}

# --- FUNCIÓN PRINCIPAL DE LA VENTANA ---
def ventana_asistente_ia(usuario, lista_usuarios):
    ventana = tk.Toplevel()
    ventana.title("🤖 Asistente IA de Diagnóstico")
    ventana.geometry("600x500")
    ventana.config(bg="#507383")
    
    # ---------------------------------------------
    # 1. CARGA DEL MODELO (Solo una vez)
    # ---------------------------------------------

    modelo_cargado = None
    
    # Define la ruta relativa al archivo .pkl.
    # Se asume que el archivo .pkl está en dataIA/modelo_asistente_mascotas.pkl
    # Y que ventana_asistente_ia.py está en views/
    
    # Ejemplo de ruta relativa (ajusta si es necesario):
    # Esto busca el archivo en una carpeta llamada 'dataIA' al mismo nivel de 'views'
    ruta_modelo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataIA", "modelo_asistente_mascotas.pkl")
    
    try:
        modelo_cargado = joblib.load(ruta_modelo)
        print("Modelo IA cargado exitosamente.")
    except FileNotFoundError:
        messagebox.showerror("Error de IA", f"No se encontró el modelo IA en: {ruta_modelo}. Asegúrate de que el archivo .pkl se movió correctamente.")
        ventana.destroy()
        return
    except Exception as e:
        messagebox.showerror("Error de IA", f"Error al cargar el modelo: {e}")
        ventana.destroy()
        return

    # ---------------------------------------------
    # 2. LÓGICA DE PREDICCIÓN
    # ---------------------------------------------
    def obtener_respuesta_ia():
        if modelo_cargado is None:
            messagebox.showerror("Error", "El modelo IA no está disponible.")
            return

        consulta_usuario = entry_consulta.get("1.0", tk.END).strip()
        
        if not consulta_usuario or len(consulta_usuario) < 5:
            messagebox.showwarning("Advertencia", "Por favor, describe los síntomas de tu mascota con detalle.")
            return
        
        # A. Limpieza de la entrada (CRUCIAL: debe ser idéntica al entrenamiento)
        consulta_limpia = limpiar_texto(consulta_usuario)
        
        if not consulta_limpia:
             messagebox.showwarning("Advertencia", "La descripción es muy corta o no contiene palabras clave.")
             return
            
       # views/ventana_asistente_ia.py (dentro de la función obtener_respuesta_ia)

# ... (código de limpieza y validación) ...
        
        try:
            # B. Predicción
            prediccion_en_ingles = modelo_cargado.predict([consulta_limpia])[0]
            
            # C. Traducción
            # Busca la traducción; si no la encuentra, usa el nombre en inglés original
            prediccion_en_espanol = TRADUCCIONES_ENFERMEDADES.get(
                prediccion_en_ingles, 
                prediccion_en_ingles # Valor por defecto si no está en el diccionario
            )
            
            # D. Formateo de Respuesta (usando la variable en español)
            respuesta = (
                f"🐾 **Diagnóstico Sugerido por la IA:**\n\n"
                f"La inteligencia artificial predice que los síntomas ingresados "
                f"son consistentes con la enfermedad de **{prediccion_en_espanol}**.\n\n" # <--- CAMBIO AQUÍ
                f"🚨 **Advertencia Importante:** Esta es solo una predicción "
                f"automática. Consulta siempre con un veterinario real para un diagnóstico definitivo."
            )
            
            lbl_resultado.config(text=respuesta, fg="#C62828") 

        except Exception as e:
            lbl_resultado.config(text=f"Error en la predicción: {e}")


    # ---------------------------------------------
    # 3. INTERFAZ GRÁFICA (Widgets)
    # ---------------------------------------------
# 1. Definir la ruta de la imagen
    ruta_imagenia = os.path.join(os.path.dirname(__file__), "imagen","image5.png")

    frame_image_izquierdo = tk.Frame(ventana, bg="#507383")
    # side="left" lo coloca a la izquierda; anchor="nw" lo alinea arriba y a la izquierda
    frame_image_izquierdo.pack(side="right", anchor="se", padx=(10, 40))
    # Usaremos un bloque try/except por si el archivo de imagen no se encuentra
    try:
        # 2. Cargar la imagen usando PIL y redimensionar
        img_pil = Image.open(ruta_imagenia).convert("RGBA")
        
        # Redimensiona la imagen a un tamaño adecuado para el espacio. 
       
        img_pil = img_pil.resize((250, 250), Image.LANCZOS)
        
        # 3. Convertir a PhotoImage para Tkinter
        logo_tk = ImageTk.PhotoImage(img_pil)
        
        # 4. Crear la etiqueta y mostrar la imagen
        lbl_imagen = tk.Label(ventana, image=logo_tk, bg="#507383")
        
        # OBLIGATORIO: Guardar una referencia a la imagen para que Tkinter no la borre
        lbl_imagen.image = logo_tk
        
        lbl_imagen.pack(side="bottom",pady=20, padx=10, fill="both", expand=True)

    except FileNotFoundError:
        # Mensaje de respaldo si la imagen no se encuentra
        tk.Label(
            ventana, 
            text="[Error: Imagen 'image1.png' no encontrada]", 
            font=("Arial", 10, "italic"), 
            bg="#507383", 
            height=10
        ).pack(pady=20, padx=10, fill="both", expand=True)
    
    

    # Título
    tk.Label(ventana, text="Asistente de Diagnóstico de Síntomas PETLY", 
             font=("cambria", 18, "bold"), bg="#507383", fg="#000000").pack(pady=15)

    # Instrucciones
    tk.Label(ventana, text="Ingresa los síntomas de tu mascota (ej: 'diarrea, vómitos, letargo'):", 
             font=("cambria", 14), bg="#507383").pack(pady=(0, 5))

    # Caja de texto para la consulta (Usamos Text para multi-línea)
    entry_consulta = tk.Text(ventana, height=5, width=60, font=("Arial", 11), bd=2, relief="sunken")
    entry_consulta.pack(pady=5, padx=20)

    # Botón de Consulta
    tk.Button(ventana, text="Analizar Síntomas 🧠", 
              command=obtener_respuesta_ia, 
              font=("cambria", 14, "bold"), bg="#BDBDBD", fg="black", 
              width=20).pack(pady=10)

    # Separador
    tk.Frame(ventana, height=2, bd=1, relief=tk.SUNKEN, bg="#BDBDBD").pack(fill="x", padx=20, pady=10)

    # Área de Resultado
    tk.Label(ventana, text="Esperando consulta...", 
             font=("cambria", 14), bg="#507383", anchor="w", justify=tk.LEFT).pack(pady=(5, 0))

    lbl_resultado = tk.Label(ventana, text="", 
                             font=("Arial", 12), bg="#FAFAFA", height=8, width=60,
                             anchor="nw", justify=tk.LEFT, wraplength=550, bd=2, relief="sunken")
    lbl_resultado.pack(pady=10, padx=20)
    
    ventana.mainloop()