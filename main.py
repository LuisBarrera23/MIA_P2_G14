from flask import Flask,jsonify,request

from flask_cors import CORS

import json

from Singleton import Singleton
from analyze import Analyze

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
    instancia.consola=""
    analizador=Analyze(entrada)
    analizador.analyze()
    return jsonify({'salida':instancia.consola})
        
@app.route('/open',methods=['POST'])
def Open():
    from Commands.Open import Open
    type=request.json['type']
    name=request.json['name']
    print(f"Esto es lo que trae el json: type={type}, name={name}")
    abrir = Open(type, None, None, name)
    abrir.verificar = True
    contenido = abrir.run()
    return jsonify({'open':contenido})    
        
@app.route('/backup',methods=['POST'])
def Backup():
    from Commands.Backup import Backup
    backup = Backup(None,None, None, None, None)
    backup.json = request.get_json()
    respuesta = backup.run()
    # print(f"Esto es lo que trae el json: type={type}, name={name}")
    return jsonify({'backup':respuesta})    
        
@app.route('/recovery',methods=['POST'])
def Recovery():
    type=request.json['type']
    name=request.json['name']
    print(f"Esto es lo que trae el json: type={type}, name={name}")
    return jsonify({'open':"Este seria el texto que contiene el archivo del bucket o server externo."})    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)