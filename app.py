from flask import Flask, render_template, request, jsonify, redirect, url_for  
from contacto import Contacto  
import database as dbase  
import pymongo  
from bson import ObjectId  

# Crea una instancia de la base de datos
db = dbase.DatabaseAgenda()

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define la ruta para la página principal
@app.route('/')
def home():
    contactos = list(db.contactos.find())  # Obtiene todos los contactos de la base de datos
    for contacto in contactos:
        contacto['_id'] = str(contacto['_id']) 
    return render_template('index.html', contactos=contactos)  

# Define la ruta para actualizar un contacto existente
@app.route('/contacto/<id>', methods=['POST'])
def actualizar_contacto(id):
    nombre = request.form['nombre']  
    edad = request.form['edad']  
    categoria = request.form['categoria']  
    telefono = request.form['telefono']  
    direccion = request.form['direccion']  
    favorito = request.form.get('favorito', 'off') == 'on'  

    # Verifica que el nombre y el teléfono no estén vacíos
    if nombre and telefono:
        if edad and not edad.isdigit():
            return notFound()
        edad = int(edad) if edad else ''  

        # Crea la lista de datos de contacto
        datos_de_contacto = [{
            'categoria': categoria,
            'telefono': int(telefono),
            'direccion': direccion
        }]
        # Actualiza el contacto en la base de datos
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

# Define la ruta para crear un nuevo contacto
@app.route('/contacto', methods=['POST'])
def nuevo_contacto():
    contacto_collection = db.contactos  
    nombre = request.form['nombre'] 
    edad = request.form.get('edad') 
    categoria = request.form.get('categoria')  
    telefono = request.form['telefono']  
    direccion = request.form.get('direccion')  
    favorito = request.form.get('favorito', 'off') == 'on'  

    # Verifica que el nombre y el teléfono no estén vacíos
    if nombre and telefono:
        # Verifica que la edad sea un número o esté vacía
        if edad and not edad.isdigit():
            return notFound()
        edad = int(edad) if edad else ''  

        # Crea la lista de datos de contacto
        datos_de_contacto = [{
            'categoria': categoria,
            'telefono': int(telefono),
            'direccion': direccion
        }]

        # Crea una instancia de Contacto y la guarda en la base de datos
        contacto = Contacto(nombre, edad, datos_de_contacto, favorito)
        contacto_collection.insert_one(contacto.to_dict())
        return redirect(url_for('home'))  
    else:
        return notFound() 

# Define la ruta para buscar contactos
@app.route('/buscar')
def buscar_contacto():
    query = request.args.get('query', '')  # Obtiene el término de búsqueda de la URL
    if query:
        # Busca contactos que coincidan con el término de búsqueda
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

# Define la ruta para mostrar los contactos favoritos
@app.route('/favoritos')
def mostrar_favoritos():
    favoritos = list(db.contactos.find({"favorito": True})) 
    return render_template('index.html', contactos=favoritos) 

# Define la ruta para mostrar todos los contactos, ordenados por favoritos primero
@app.route('/todos_contactos')
def todos_contactos_favoritos_primero():
    contactos = list(db.contactos.find().sort([("favorito", pymongo.DESCENDING)]))  
    return render_template('index.html', contactos=contactos)  

# Define la ruta para eliminar un contacto
@app.route('/eliminar_contacto/<id>', methods=['POST'])
def eliminar_contacto(id):
    if not ObjectId.is_valid(id):
        return notFound()  
    query = {"_id": ObjectId(id)}
    db.contactos.delete_one(query)  
    return redirect(url_for('home')) 

# Maneja los errores 404
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=1200)
