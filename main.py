from flask import Flask,jsonify,request

from flask_cors import CORS

import json

from Singleton import Singleton
from Commands.Create import Create
from Commands.Transfer import Transfer
from Commands.Rename import Rename
from Commands.Modify import Modify
from Commands.DeleteAll import DeleteAll

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
    # create=Create("hola.txt", "esta es una prueba 1", "carpeta1","server")
    # create.run()
    # create=Create("hola2.txt", "esta es una prueba 2", "carpeta 2","server")
    # create.run()
    # transfer=Transfer("carpeta 2","carpeta2","server","server")
    # transfer.run()
    # rename=Rename("carpeta0","carpeta 2","server")
    # rename.run()
    # modify=Modify("carpeta2/hola.txt","cambio de contenido", "server")
    # modify.run()
    deleteall=DeleteAll("bucket")
    deleteall.run()
    # app.run(host="0.0.0.0",port=8080,debug=True)