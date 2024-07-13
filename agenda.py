import pymongo
from bson import ObjectId

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

    def fetch_one(self):
        try:
            id = input("Ingrese el ID del contacto a buscar: ")
            data = self.collection.find_one({'_id': ObjectId(id)})
            if data:
                print(f'Contacto encontrado: {data}')
            else:
                print('Contacto no encontrado.')
        except Exception as e:
            print(f"Error al buscar el contacto: {e}")

    def search(self):
        try:
            buscar_filtro = input("Ingrese el nombre o teléfono para buscar: ")
            query = {
                "$or": [
                    {"nombre": {"$regex": buscar_filtro, "$options": "i"}},
                    {"datos_de_contacto.telefono": {"$regex": buscar_filtro, "$options": "i"}}
                ]
            }
            resultados = self.collection.find(query)
            resultado_encontrado = False
            for resultado in resultados:
                print(f'Contacto encontrado: {resultado}')
                resultado_encontrado = True
            if not resultado_encontrado:
                print('No se encontraron contactos con esa búsqueda.')
        except Exception as e:
            print(f"Error al buscar el contacto: {e}")

def menu():
    agenda = DatabaseAgenda()
    while True:
        print("\nMenu:")
        print("1. Insertar contacto")
        print("2. Buscar contacto por ID")
        print("3. Buscar contacto por nombre o teléfono")
        print("4. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            agenda.insert()
        elif choice == '2':
            agenda.fetch_one()
        elif choice == '3':
            agenda.search()
        elif choice == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

menu()
