import kagglehub
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import joblib

# ----------------------------------------------------
# 📌 BLOQUE DE SOLUCIÓN NLTK
# ----------------------------------------------------

# 1. Definir la ruta local para los datos de NLTK (ej. una carpeta 'nltk_data' al lado de train_ia_model.py)
nltk_data_path = os.path.join(os.path.dirname(__file__), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# 2. Añadir esta nueva ruta al path de búsqueda de NLTK
nltk.data.path.append(nltk_data_path)

print("Descargando o verificando recursos de NLTK...")
try:
    # 3. Intentar descargar los recursos a la ruta controlada
    nltk.download('punkt', download_dir=nltk_data_path, quiet=True)
    nltk.download('stopwords', download_dir=nltk_data_path, quiet=True)
    print("✅ Recursos de NLTK listos para usar.")
except Exception as e:
    print(f"❌ Error al intentar descargar recursos de NLTK: {e}")
# ----------------------------------------------------

# ... el resto de tu código continúa aquí...
# Descargar la última versión del dataset 'animal-disease-prediction'
print("\nDescargando el dataset de Kaggle Hub...")

# ...
# Y así sucesivamente
# ...

# Descargar la última versión del dataset 'animal-disease-prediction'
print("Descargando el dataset de Kaggle Hub...")
path = kagglehub.dataset_download("shijo96john/animal-disease-prediction")

# La variable 'path' ahora contiene la ruta de la CARPETA donde están los archivos.
# Convertimos el objeto path a una cadena de texto para usarlo con os.listdir
ruta_directorio = str(path)

print("\nPath de la carpeta donde se descargó:", ruta_directorio)

# Listamos el contenido de esa carpeta para encontrar el nombre del archivo CSV
print("\nArchivos encontrados en la carpeta:")
for filename in os.listdir(ruta_directorio):
    print(f"- {filename}")

# 📌 Definimos el nombre exacto del archivo CSV
nombre_archivo_csv = "cleaned_animal_disease_prediction.csv"

# Unimos la ruta de la carpeta con el nombre del archivo para obtener la ruta completa
ruta_completa_csv = os.path.join(ruta_directorio, nombre_archivo_csv)

# Cargamos el DataFrame usando la ruta completa
try:
    df = pd.read_csv(ruta_completa_csv)
    print("\n✅ DataFrame cargado exitosamente.")

    # Muestra información clave para la siguiente fase de IA
    print("\nInformación del DataFrame:")
    df.info()
   # Muestra todas las columnas y sus tipos de datos
    print(df.info())

except Exception as e:
    print(f"\n❌ Ocurrió un error al cargar el CSV: {e}")

# Muestra todas las columnas y sus tipos de datos
print(df.info())

# Lista de columnas que describen los síntomas (Symptom_1, Symptom_2, etc., más las binarias)
symptom_columns = [
    'Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
    'Appetite_Loss', 'Vomiting', 'Diarrhea', 'Coughing',
    'Labored_Breathing', 'Lameness', 'Skin_Lesions', 'Nasal_Discharge',
    'Eye_Discharge'
]

# Crear una nueva columna combinando todas las descripciones de síntomas en una sola cadena de texto
# NOTA: Solo incluimos los síntomas binarios ('Yes'/'No') si son 'Yes'.
def combine_symptoms(row):
    combined = []

    # 1. Añadir los síntomas descriptivos (Symptom_1 a Symptom_4)
    for col in ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4']:
        if row[col] not in ['No', 'None', 'Normal']: # Evitar palabras vacías
            combined.append(row[col])

    # 2. Añadir los síntomas binarios (Appetite_Loss, Vomiting, etc.) si el valor es 'Yes'
    for col in ['Appetite_Loss', 'Vomiting', 'Diarrhea', 'Coughing',
                'Labored_Breathing', 'Lameness', 'Skin_Lesions', 'Nasal_Discharge',
                'Eye_Discharge']:
        if row[col] == 'Yes':
            # Añadimos el nombre de la columna para indicar el síntoma
            combined.append(col.replace('_', ' '))

    return " ".join(combined)

df['Symptoms_Combined'] = df.apply(combine_symptoms, axis=1)

print("\nPrimeros 5 síntomas combinados:")
print(df['Symptoms_Combined'].head(9))

stop_words = set(stopwords.words('english'))

def limpiar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    # Eliminar puntuación, comas, etc.
    texto = re.sub(r'[^a-z\s]', '', texto)
    tokens = word_tokenize(texto)
    # Eliminar stopwords y palabras muy cortas
    tokens_limpios = [w for w in tokens if not w in stop_words and len(w) > 2]
    return " ".join(tokens_limpios)

# Aplicar la limpieza a la nueva columna combinada
df['Symptoms_clean'] = df['Symptoms_Combined'].apply(limpiar_texto)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# 1. Definir X y Y (usando el nombre de columna CORRECTO)
X = df['Symptoms_clean']        # Columna de entrada limpia
Y = df['Disease_Prediction']    # Columna de salida (etiquetas)

# 2. Separar datos (20% para prueba)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42,
    stratify=Y
)

# 3. Crear el Pipeline (Vectorizador + Clasificador)
modelo_ia = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)

# 4. Entrenar
print("\nIniciando el entrenamiento del modelo...")
modelo_ia.fit(X_train, y_train)
print("✅ Entrenamiento completado.")

# 5. Evaluar
predicciones = modelo_ia.predict(X_test)
print("\nReporte de Clasificación (Precisión, Recall, F1-Score):")
print(classification_report(y_test, predicciones, zero_division=0))

# 6. Guardar el modelo entrenado
joblib.dump(modelo_ia, 'modelo_asistente_mascotas.pkl')
print("\nModelo guardado como 'modelo_asistente_mascotas.pkl'.")