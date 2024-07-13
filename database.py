import pymongo

class DatabaseAgenda:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["agenda"]
            print("Conectado a MongoDB y colección contactos.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
