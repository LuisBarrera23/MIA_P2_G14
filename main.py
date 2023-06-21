from flask import Flask,jsonify,request

from flask_cors import CORS

import json

from Singleton import Singleton

app = Flask(__name__)
CORS(app)


@app.route('/',methods=['GET'])
def inicializacion():
    return("<h1>Servidor Corriendo con exito</h1>")

@app.route('/login',methods=['POST'])
def login():
    usuario=request.json['user']
    contraseña=request.json['password']
    instancia=Singleton.getInstance()
    if(instancia.checkUsuario(usuario,contraseña)):
        return jsonify({'acceso':"autorizado"})
    else:
        return jsonify({'acceso':"denegado"})
    
@app.route('/analizar',methods=['POST'])
def analizar():
    entrada=request.json['entrada']
    instancia=Singleton.getInstance()
    return jsonify({'salida':"xd"})
        
    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)