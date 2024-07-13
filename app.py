from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from contacto import Contacto
import database as dbase

db = dbase.DatabaseAgenda()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/Contacto', methods=['POST'])
def nuevo_contacto():
    contacto = db['contactos']
    nombre = request.form['nombre']
    edad = request.fomr['edad']
    categoria = request.form['categoria']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    favorito = request.form['favorito']

    if nombre and edad and categoria and telefono and direccion and favorito:
        contacto = Contacto(nombre,edad,categoria,telefono,direccion,favorito)
        contacto.insert_one(contacto.to_dict())
        response = jsonify({
            'nombre': nombre,
            'edad': edad,
            'categoria': categoria,
            'telefono': telefono,
            'direccion': direccion,
            'favorito': favorito
        })
        return redirect(url_for('home'))
    else:
        return notFound()
    


@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado '+ request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == '__main__':
    app.run(debug=True,port=1200)
