from datetime import datetime


class Turno:
    def __init__(self, fecha, hora, motivo, veterinario="general"):
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.veterinario = veterinario

    def obtener_datetime(self):
        """Devuelve la fecha y hora combinadas como un objeto datetime."""
        fecha_hora_str = f"{self.fecha} {self.hora}"
        return datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")

