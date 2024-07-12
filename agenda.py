import pymongo

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    database = client["agenda"]
    print("conectado a mongo")

except Exception as e:
    print("error mongo")