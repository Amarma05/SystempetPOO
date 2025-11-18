class Mascota:
    def __init__(self, nombre, fecha_nac, raza, sexo, peso, vacunas):
        self.nombre = nombre
        self.fecha_nac = fecha_nac
        self.raza = raza
        self.sexo = sexo
        self.peso = peso
        self.vacunas = vacunas
        self.turnos = []
#funcion para agregar los turnos a cada mascota y se guardan en una lista
    def agregar_turno(self, turno):
        self.turnos.append(turno)
#mostramos los datos de la mascota y los turnos   
    def mostrar_info(self):
        """Muestra los datos completos de la mascota"""
        print(f"🐾 Nombre: {self.nombre}")
        print(f"   Fecha de nacimiento: {self.fecha_nac}")
        print(f"   Raza: {self.raza}")
        print(f"   Sexo: {self.sexo}")
        print(f"   Peso: {self.peso} kg")
        print(f"   Vacunas: {self.vacunas}")
        print(f"   Turnos: {len(self.turnos)} registrados\n")