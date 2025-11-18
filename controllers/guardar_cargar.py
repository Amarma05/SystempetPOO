import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import json
from models.usuario import Usuario
from models.mascota import Mascota
from models.turno import Turno


# Función para guardar datos a la lista (SIMPLIFICADA)
# ⚠️ REEMPLAZA TU FUNCION EXISTENTE CON ESTA ⚠️
def guardar_datos(usuarios):
    """Convierte la lista completa de objetos Usuario a JSON y la guarda."""
    
    data_nueva = []
    for u in usuarios:
        # Serializa el objeto Usuario (u) a un diccionario
        data_nueva.append({
            "nombre": u.nombre,
            "fecha_de_nacimiento": u.fecha_de_nacimiento,
            "dni": u.dni,
            "email": u.email,
            "telefono": u.telefono,
            "mascotas": [
                {
                    "nombre": m.nombre,
                    "fecha_nac": m.fecha_nac,
                    "raza": m.raza,
                    "sexo": m.sexo,
                    "peso": m.peso,
                    "vacunas": m.vacunas,
                    "turnos": [
                        {
                            "fecha": t.fecha,
                            "hora": t.hora,
                            "motivo": t.motivo,
                            "veterinario": t.veterinario
                        } for t in m.turnos
                    ]
                } for m in u.mascotas
            ]
        })

    # Guarda la lista completa (data_nueva), sobreescribiendo el archivo
    with open("usuarios.json", "w") as f:
        json.dump(data_nueva, f, indent=4)


# Función para cargar los datos guardados (MANTENER COMO ESTA)
def cargar_datos():
    try:
        with open("usuarios.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    
    usuarios = []
    for d in data:
        u = Usuario(d["nombre"], d["fecha_de_nacimiento"], d["dni"], d["email"], d["telefono"])

        for m in d.get("mascotas", []):
            mascota = Mascota(m["nombre"], m["fecha_nac"], m["raza"], m["sexo"], m["peso"], m["vacunas"])
    
            for t in m.get("turnos", []):
                turno = Turno(t["fecha"], t["hora"], t["motivo"], t["veterinario"])
                mascota.agregar_turno(turno)
                
            u.agregar_mascota(mascota)
        usuarios.append(u)
    
    return usuarios