import pymongo

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