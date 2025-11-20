from datetime import datetime
from models.usuario import Usuario


def obtener_y_ordenar_turnos(usuario):
    """
    Recorre todas las mascotas del usuario, recoge sus turnos, 
    y los ordena cronológicamente, excluyendo turnos pasados.
    """
    turnos_actuales = []
    now = datetime.now() 
    
    for mascota in usuario.mascotas:
        for turno in mascota.turnos:
            try:
                # El formato debe coincidir con el que guardas: DD/MM/AAAA HH:MM
                #fecha_hora_str = f"{turno.fecha} {turno.hora}"
                #fecha_turno = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
                fecha_hora_dt = turno.obtener_datetime()
                if fecha_hora_dt >= now:
                    turnos_actuales.append({
                        "mascota": mascota.nombre,
                        "fecha_hora": fecha_hora_dt,
                        "info": turno
                    })
            except ValueError:
                # Manejo de errores de formato
                continue
                
    turnos_actuales.sort(key=lambda x: x["fecha_hora"])
    
    return turnos_actuales