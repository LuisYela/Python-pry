from flask import Flask, request
from flask_pymongo import PyMongo
import redis

app=Flask(__name__)
app.config["MONGO_URI"]='mongodb://35.223.184.245:27017/datosCorona'
mongo=PyMongo(app)
cliente=redis.Redis(host='35.223.184.245', port=6379)

@app.route('/datos', methods=['POST'])
def crear_dato():
    #
    print(request.json)
    Nombre=request.json['Nombre']
    Departamento=request.json['Departamento']
    Edad=request.json['Edad']
    Forma_contagio=request.json['Forma_contagio']
    Estado=request.json['Estado']

    if Nombre and Departamento and Edad and Forma_contagio and Estado:
        #
        id = mongo.db.coronas.insert(
            {'Nombre':Nombre, 'Departamento':Departamento, 'Edad':Edad, 'Forma_contagio':Forma_contagio, 'Estado':Estado}
        )
        cliente.hmset(name='datosCovid', mapping={'Nombre':Nombre, 'Departamento':Departamento, 'Edad':Edad, 'Forma_contagio':Forma_contagio, 'Estado':Estado})
        if Edad<=30:
            cliente.incr(name='0-30')
        elif Edad>30 and Edad<=40:
            cliente.incr(name='31-40')
        elif Edad>40 and Edad<=50:
            cliente.incr(name='41-50')
        elif Edad>50 and Edad<=60:
            cliente.incr(name='51-60')
        elif Edad>60 and Edad<=70:
            cliente.incr(name='61-70')
        elif Edad>70 and Edad<=80:
            cliente.incr(name='71-80')
        else:
            cliente.incr(name='mayores_a_80')
        respose={
            'id':str(id),
            'Nombre':Nombre,
            'Departamento':Departamento,
            'Edad':Edad,
            'Forma_contagio':Forma_contagio,
            'Estado':Estado
        }
        return respose
    else:
        {'message':'error_faltan_datos'}
    return {'message':'recibido'}

@app.route('/pruebas', methods=['POST'])
def preba_crear_dato():
    #
    print(request.json)
    Nombre=request.json['Nombre']
    Departamento=request.json['Departamento']
    Edad=request.json['Edad']
    Forma_contagio=request.json['Forma_contagio']
    Estado=request.json['Estado']

    if Nombre and Departamento and Edad and Forma_contagio and Estado:
        #
        respose={
            'id':str(id),
            'Nombre':Nombre,
            'Departamento':Departamento,
            'Edad':Edad,
            'Forma_contagio':Forma_contagio,
            'Estado':Estado
        }
        return respose
    else:
        {'message':'error_faltan_datos'}
    return {'message':'recibido'}

@app.route('/')
def saludar():
    #
    return "Hola desde el servidor"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)
