import pymongo



class DatabaseAgenda:
        
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        db = client["agenda"]
        print("conectado a mongo")

    except Exception as e:
        print("error mongo")


    try:
        collection = db["contactos"]
        print("conecado a contactos")

    except Exception as e:
        print("error")


    def insert(self, contactos):
        try:
            data = {
                '_id':contactos.cid,
                'nombre': contactos.nombre,
                'edad': contactos.edad,
                'datos_de_contacto': [
                    {
                        'categoria': contactos.categoria,
                        'direccion': contactos.direccion,
                        'telefono': contactos.telefono
                    }
                ] ,
                'favorito': contactos.favorito

            }
        
            cid = self.collection.insert_one(data).inserted_id
            print('Contacto insertado ID:{cid}')
        except Exception as e:
            print("error: {e}")

    def fetch_one(self, cid):
        data = self.collection.find_one({'_id': cid})
        return data

    def fetch_all(self):
        data = self.collection.find()
        return data

    def update(self, cid, contactos):
        data = {
            '_id':contactos.cid,
            'nombre': contactos.nombre,
            'edad': contactos.edad,
            'datos_de_contacto': [
                    {
                        'categoria': contactos.categoria,
                        'direccion': contactos.direccion,
                        'telefono': contactos.telefono
                    }
                ] ,
                'favorito': contactos.favorito
    }
        self.collection.update_one({'_id':cid}, {'$set': data})


    def delete(self, cid):
        self.collection.delete_one({'_id':cid})

