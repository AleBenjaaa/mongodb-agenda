class Contacto:
    def __init__(self, nombre, edad, datos_de_contacto, favorito):
        self.nombre = nombre
        self.edad = edad
        self.datos_de_contacto = datos_de_contacto
        self.favorito = favorito

    def from_form(self, form):
        self.nombre = form.get('nombre')
        self.edad = form.get('edad')
        self.datos_de_contacto = [{
            'categoria': form.get('categoria'),
            'telefono': form.get('telefono'),
            'direccion': form.get('direccion')
        }]
        self.favorito = form.get('favorito') == 'on'

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'datos_de_contacto': self.datos_de_contacto,
            'favorito': self.favorito
        }
