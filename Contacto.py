class Contacto:
    def __init__(self, nombre, edad, datos_de_contacto, favorito):
        self.nombre = nombre
        self.edad = edad
        self.datos_de_contacto = datos_de_contacto
        self.favorito = favorito

    @classmethod
    def user_input(cls):
        nombre = input('Ingrese el nombre de contacto: ')
        edad = input('Ingrese la edad: ')

        categoria = input('Ingrese la categoría de contacto (personal/trabajo, etc.): ')
        direccion = input('Ingrese la dirección: ')
        telefono = input('Ingrese el teléfono: ')
        datos_de_contacto = [
            {
                'categoria': categoria,
                'direccion': direccion,
                'telefono': telefono
            }
        ]

        def favorito_bool():
            while True:
                favorito = input('Contacto favorito (si/no): ').lower()
                if favorito in ['si', 'no']:
                    return favorito == 'si'
                print('!Error el tipo de dato debe ser si o no')

        favorito = favorito_bool()

        return cls(nombre, edad, datos_de_contacto, favorito)
    
    def __str__(self):
        return f'Nombre: {self.nombre}, Edad: {self.edad}, Datos de contacto: {self.datos_de_contacto}, Favorito: {self.favorito}'
