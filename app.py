from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from contacto import Contacto
import database as dbase

db = dbase.DatabaseAgenda()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacto', methods=['POST'])
def nuevo_contacto():
    contacto_collection = db.contactos  # Asegúrate de acceder al atributo correcto
    nombre = request.form['nombre']
    edad = request.form['edad']  # Corregido el error tipográfico aquí
    categoria = request.form['categoria']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    favorito = request.form.get('favorito', 'off') == 'on'  # Usar get() con valor predeterminado

    if nombre and edad and categoria and telefono and direccion:
        datos_de_contacto = [{
            'categoria': categoria,
            'telefono': telefono,
            'direccion': direccion
        }]
        contacto = Contacto(nombre, edad, datos_de_contacto, favorito)
        contacto_collection.insert_one(contacto.to_dict())  # Cambiado a contacto_collection
        response = jsonify({
            'nombre': nombre,
            'edad': edad,
            'datos_de_contacto': datos_de_contacto,
            'favorito': favorito
        })
        return redirect(url_for('home'))
    else:
        return notFound()

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
