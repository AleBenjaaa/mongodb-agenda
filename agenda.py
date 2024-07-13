import pymongo



class DatabaseAgenda:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["agenda"]
            self.collection = self.db["contactos"]
            print("Conectado a MongoDB y colección contactos.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    def user_input(self):
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

        return {
            'nombre': nombre,
            'edad': edad,
            'datos_de_contacto': datos_de_contacto,
            'favorito': favorito
        }

    def insert(self):
        try:
            data = self.user_input()
            inserted_id = self.collection.insert_one(data).inserted_id
            print(f'Contacto insertado ID: {inserted_id}')
        except Exception as e:
            print(f"Error al insertar el contacto: {e}")



agenda = DatabaseAgenda()
agenda.insert()
    # def fetch_one(self, cid):
    #     data = self.collection.find_one({'_id': cid})
    #     return data

    # def fetch_all(self):
    #     data = self.collection.find()
    #     return data

    # def update(self, contactos):
    #     data = {
    #         'nombre': contactos.nombre,
    #         'edad': contactos.edad,
    #         'datos_de_contacto': [
    #                 {
    #                     'categoria': contactos.categoria,
    #                     'direccion': contactos.direccion,
    #                     'telefono': contactos.telefono
    #                 }
    #             ] ,
    #             'favorito': contactos.favorito
    # }
    #     self.collection.update_one( {'$set': data})


    # def delete(self, cid):
    #     self.collection.delete_one({'_id':cid})

