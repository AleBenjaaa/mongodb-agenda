class Contacto:
    def __init__(self, nombre, edad, categoria, telefono, direccion, favorito):
        self.nombre = nombre
        self.edad = edad
        self.categoria = categoria
        self.telefono = telefono
        self.direccion = direccion
        self.favorito = favorito

    def from_form(self, form):
        self.nombre = form.get('nombre')
        self.edad = form.get('edad')
        self.categoria = form.get('categoria')
        self.telefono = form.get('telefono')
        self.direccion = form.get('direccion')
        self.favorito = form.get('favorito') == 'on' 

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'categoria': self.categoria,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'favorito': self.favorito
        }
