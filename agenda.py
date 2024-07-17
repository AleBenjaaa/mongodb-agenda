import pymongo
from bson import ObjectId

# Prueba de funcionamiento de pymongo, el trabajo final es app.py <3

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
        edad = int(input('Ingrese la edad: '))
        categoria = input('Ingrese la categoría de contacto: ')
        direccion = input('Ingrese la dirección: ')
        telefono = int(input('Ingrese el teléfono: '))
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

    def eliminar_contacto(self):
        try:
            opcion = input("Ingrese el ID, nombre o número de teléfono del contacto a eliminar: ")

            if ObjectId.is_valid(opcion):
                resultado = self.collection.delete_one({'_id': ObjectId(opcion)})
                if resultado.deleted_count == 1:
                    print(f"Contacto con ID {opcion} eliminado correctamente.")
                    return

            resultado = self.collection.delete_many({"nombre": opcion})
            if resultado.deleted_count > 0:
                print(f"Se eliminaron {resultado.deleted_count} contactos con el nombre: {opcion}.")
                return

            resultado = self.collection.delete_many({"datos_de_contacto.telefono": opcion})
            if resultado.deleted_count > 0:
                print(f"Se eliminaron {resultado.deleted_count} contactos con el teléfono: {opcion}.")
                return

            print(f"No se encontraron contactos con el nombre o teléfono: {opcion}.")
        
        except Exception as e:
            print(f"Error al eliminar el contacto: {e}")

    def modificar_contacto(self):
        try:
            opcion = input("Ingrese el nombre o número de teléfono del contacto a modificar: ")

            if ObjectId.is_valid(opcion):
                contacto = self.collection.find_one({'_id': ObjectId(opcion)})
            else:
                contacto = self.collection.find_one({"$or": [{"nombre": opcion}, {"datos_de_contacto.telefono": opcion}]})

            if contacto:
                print(f'Contacto encontrado: {contacto}')

                nueva_categoria = input('Ingrese la nueva categoría de contacto: ')
                nueva_direccion = input('Ingrese la nueva dirección: ')
                nuevo_telefono = int(input('Ingrese el nuevo teléfono: '))

                nuevo_datos_de_contacto = [{
                    'categoria': nueva_categoria,
                    'direccion': nueva_direccion,
                    'telefono': nuevo_telefono
                }]

                contacto['datos_de_contacto'] = nuevo_datos_de_contacto
                resultado = self.collection.replace_one({'_id': contacto['_id']}, contacto)

                if resultado.modified_count == 1:
                    print(f'Contacto modificado correctamente.')
                else:
                    print(f'No se pudo modificar el contacto.')

            else:
                print(f"No se encontró ningún contacto con el nombre o teléfono: {opcion}.")

        except Exception as e:
            print(f"Error al modificar el contacto: {e}")


def menu():
    agenda = DatabaseAgenda()
    while True:
        print("\nMenu:")
        print('Prueba de funcionamiento de pymongo, el trabajo final es app.py <3')
        print("1. Insertar contacto")
        print("2. Buscar contacto por ID, nombre o teléfono")
        print('3. Listar contactos')
        print("4. Eliminar contacto por nombre o teléfono")
        print("5. Modificar contacto por nombre o teléfono")
        print("0. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == '1':
            agenda.insert()
        elif choice == '2':
            agenda.filtro_de_busqueda()
        elif choice == '3':
            agenda.listar_agenda()
        elif choice == '4':
            agenda.eliminar_contacto()
        elif choice == '5':
            agenda.modificar_contacto()
        elif choice == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

menu()
