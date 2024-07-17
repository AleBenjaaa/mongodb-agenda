class Contacto:
    def __init__(self, nombre, edad, datos_de_contacto, favorito):
        self.nombre = nombre
        self.edad = edad
        self.datos_de_contacto = datos_de_contacto
        self.favorito = favorito

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'datos_de_contacto': self.datos_de_contacto,
            'favorito': self.favorito
        }
    