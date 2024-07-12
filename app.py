from Contacto import Contacto
from agenda import DatabaseAgenda

database = DatabaseAgenda


def app():
    while True:
        print('Menu: ')
        print('[1] Ingresar nuevo contacto')
        print('[2] Mostrar todos los contacto')
        print('[3] Buscar contacto')
        print('[4] Actualizar informacion de un contacto')
        print('[5] Eliminar un contacto')
        print('[0] Salir')

        try:
            choice = int(input("> "))

            if choice == 1:
                contacto = Contacto.user_input()
                database.insert(contacto)
            elif choice == 2:
                data = database.fetch_all()
                for contacto in data:
                    print(contacto)

            elif choice == 0:
                break
            else:
 
                print("Opcion invalida")

        except Exception as e:
            print(e)
            print("Contacto invalido")


if __name__ == "__main__":

    app()
