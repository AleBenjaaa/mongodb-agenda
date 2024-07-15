from flask import Flask, render_template, request, jsonify, redirect, url_for
from contacto import Contacto
import database as dbase
import pymongo
from bson import ObjectId  

db = dbase.DatabaseAgenda()

app = Flask(__name__)

@app.route('/')
def home():
    contactos = list(db.contactos.find())
    for contacto in contactos:
        contacto['_id'] = str(contacto['_id'])  
    return render_template('index.html', contactos=contactos)

@app.route('/contacto/<id>', methods=['POST'])
def actualizar_contacto(id):
    nombre = request.form['nombre']
    edad = request.form['edad']
    categoria = request.form['categoria']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    favorito = request.form.get('favorito', 'off') == 'on'

    if nombre and edad and categoria and telefono and edad.isdigit():
        edad = int(edad) 
        datos_de_contacto = [{
            'categoria': categoria,
            'telefono': telefono,
            'direccion': direccion
        }]
        db.contactos.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": nombre,
                "edad": edad,
                "datos_de_contacto": datos_de_contacto,
                "favorito": favorito
            }}
        )
        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/contacto', methods=['POST'])
def nuevo_contacto():
    contacto_collection = db.contactos
    nombre = request.form['nombre']
    edad = request.form['edad']
    categoria = request.form['categoria']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    favorito = request.form.get('favorito', 'off') == 'on'

    if nombre and edad and categoria and telefono and edad.isdigit():
        edad = int(edad)  
        datos_de_contacto = [{
            'categoria': categoria,
            'telefono': telefono,
            'direccion': direccion
        }]
        contacto = Contacto(nombre, edad, datos_de_contacto, favorito)
        contacto_collection.insert_one(contacto.to_dict())
        return redirect(url_for('home'))
    else:
        return notFound()

@app.route('/buscar')
def buscar_contacto():
    query = request.args.get('query', '')
    if query:
        contactos = list(db.contactos.find({
            "$or": [
                {"nombre": {"$regex": query, "$options": "i"}},
                {"edad": {"$regex": query, "$options": "i"}},
                {"datos_de_contacto.telefono": {"$regex": query, "$options": "i"}},
                {"datos_de_contacto.direccion": {"$regex": query, "$options": "i"}},
                {"datos_de_contacto.categoria": {"$regex": query, "$options": "i"}}
            ]
        }))
    else:
        contactos = list(db.contactos.find())

    return render_template('index.html', contactos=contactos)

@app.route('/favoritos')
def mostrar_favoritos():
    favoritos = list(db.contactos.find({"favorito": True}))
    return render_template('index.html', contactos=favoritos)

@app.route('/todos_contactos')
def todos_contactos_favoritos_primero():
    contactos = list(db.contactos.find().sort([("favorito", pymongo.DESCENDING)]))
    return render_template('index.html', contactos=contactos)

@app.route('/eliminar_contacto/<id>', methods=['POST'])
def eliminar_contacto(id):
    if not ObjectId.is_valid(id):
        return notFound()
    query = {"_id": ObjectId(id)}
    db.contactos.delete_one(query)
    return redirect(url_for('home'))

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=1200)
