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

    def filtro_de_busqueda(self):
        try:
            buscar_filtro = input("Ingrese el ID, nombre o teléfono para buscar: ")
            query = {
                "$or": [
                    {'_id': ObjectId(buscar_filtro) if ObjectId.is_valid(buscar_filtro) else None},
                    {"nombre": {"$regex": buscar_filtro, "$options": "i"}},
                    {"datos_de_contacto.telefono": {"$regex": buscar_filtro, "$options": "i"}}
                ]
            }
            # Eliminar valores None de la consulta
            query["$or"] = [q for q in query["$or"] if q]
            
            resultados = self.collection.find(query)
            resultado_encontrado = False
            for resultado in resultados:
                print(f'Contacto encontrado: {resultado}')
                resultado_encontrado = True
            if not resultado_encontrado:
                print('No se encontraron contactos con esa búsqueda.')
        except Exception as e:
            print(f"Error al buscar el contacto: {e}")
    
    def listar_agenda(self):
        try:
            resultados = self.collection.find().sort([("favorito", pymongo.DESCENDING)])
            resultado_encontrado = False
            for resultado in resultados:
                print(f'Contacto encontrado: {resultado}')
                resultado_encontrado = True
            if not resultado_encontrado:
                print('No hay contactos agendados.')
        except Exception as e:
            print(f"Error al listar los contactos: {e}")

def menu():
    agenda = DatabaseAgenda()
    while True:
        print("\nMenu:")
        print("1. Insertar contacto")
        print("2. Buscar contacto por ID, nombre o teléfono")
        print('3. Listar contactos')
        print("0. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            agenda.insert()
        elif choice == '2':
            agenda.filtro_de_busqueda()
        elif choice == '3':
            agenda.listar_agenda()
        elif choice == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

menu()
