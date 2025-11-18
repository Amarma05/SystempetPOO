# moduloIA.py (Refactorizado)
import random
from models.turno import Turno

# --- Lista simulada de profesionales y horarios ---
PROFESIONALES = ["Dr. Vallejos Silvia", "Dra. Gomez Ana", "Dr. Perez Juan"]
HORARIOS = ["09:00","09:30","10:00","10:30","11:00","11:300","12:00","12:30","13:00", "13:30", "14:00","14:30","15:00", "15:30", "16:00"]
"""Especialidad= [
    {

    "Dr. Vallejos Silvia" = infectologia,
    "Dra. Gomez Ana" = cardiologia,
    "Dr. Perez Juan" = esterilizacion,

    }
    ]  
""" 
def generar_fecha_aleatoria(dias_futuro=7):
    """Genera una fecha en los próximos N días para la simulación."""
    from datetime import datetime, timedelta
    fecha_base = datetime.now() + timedelta(days=1)
    fecha_simulada = fecha_base + timedelta(days=random.randint(0, dias_futuro))
    return fecha_simulada.strftime("%d/%m/%Y")

def Prediccion_turnos(preferencia_hora, preferencia_profesional,preferencia_especialidad):
    """
    Simula la búsqueda y recomendación de un turno basado en preferencias.
    
    En un sistema real, aquí se consultaría una base de datos o algoritmo de IA.
    """
    
    # 1. Aplicar filtro de Profesional (si aplica)
    profesional_elegido = ""
    if preferencia_profesional and preferencia_profesional in PROFESIONALES:
        profesional_elegido = preferencia_profesional
    else:
        # Elegir uno aleatorio si no se especificó o no se encontró
        profesional_elegido = random.choice(PROFESIONALES)
        
    # 2. Aplicar filtro de Horario (simulado: buscar uno que se acerque)
    hora_recomendada = ""
    if preferencia_hora == "mañana":
        hora_recomendada = random.choice([h for h in HORARIOS if h < "12:00"])
    elif preferencia_hora == "tarde-noche":
        hora_recomendada = random.choice([h for h in HORARIOS if h >= "12:00"])
    else:
        hora_recomendada = random.choice(HORARIOS)

    # 3. Generar la recomendación simulada
    fecha_recomendada = generar_fecha_aleatoria()
    motivo_simulado = "Consulta General (Recomendación IA)"

    # Crear el objeto Turno recomendado (sin guardarlo aún)
    turno_recomendado = Turno(
        fecha=fecha_recomendada,
        hora=hora_recomendada,
        motivo=motivo_simulado,
        veterinario=profesional_elegido
    )

    return turno_recomendado