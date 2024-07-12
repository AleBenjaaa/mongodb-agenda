class Contacto:
    def __init__(self, cid, nombre, edad, datos_de_contacto, favorito):
        self.cid = cid
        self.nombre = nombre
        self.edad = edad
        self.datos_de_contacto = datos_de_contacto
        self.favorito = favorito

    
    @classmethod
    def user_input(cls):
        nombre = input('Ingrese el nombre de contacto: ')
        edad = input('Ingrese la edad: ')
        def favorito_bool():
            favorito = input('Contacto favorito: si/no')
            while favorito not in ['True','False']:
                return '!Error el tipo de dato debe ser booleano'
            return favorito
        favorito = favorito_bool()

        return cls(nombre,edad,favorito)