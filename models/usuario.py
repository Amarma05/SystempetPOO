class Usuario:
    def __init__(self, nombre,fecha_de_nacimiento, dni, email, telefono):
        self.nombre = nombre
        self.fecha_de_nacimiento = fecha_de_nacimiento
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.mascotas = []  # lista de objetos Mascota
#creamos una funcion donde las mascotas registradas entren en la lista
    def agregar_mascota(self, mascotas):
        self.mascotas.append(mascotas)
#muestra los datos del usuario y las mascotas que tiene
    def mostrar_info(self):
        print(f"Usuario: {self.nombre} | {self.fecha_de_nacimiento} | DNI: {self.dni} | Email: {self.email} | Tel: {self.telefono}")
        print("Mascotas:")
        for m in self.mascotas:
            print(f" - {m.nombre} ({m.raza})")