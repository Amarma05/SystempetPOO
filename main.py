import sys, os

# Agregamos la carpeta principal al path para importar correctamente
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importamos la función que abre la ventana de login
from views.login import iniciar_login


if __name__ == "__main__":
    iniciar_login()  # 🚀 Inicia la aplicación
 