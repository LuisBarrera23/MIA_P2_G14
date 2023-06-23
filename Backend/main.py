from flask import Flask,jsonify,request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/',methods=['GET'])
def inicializacion():
    return("<h1>Backend corriendo con exito en el puerto 5000</h1>")

@app.route('/open',methods=['POST'])
def Open():
    type=request.json['type']
    name=request.json['name']
    print(f"Esto es lo que trae el json: type={type}, name={name}")
    return jsonify({'open':"Este seria el texto que contiene el archivo del bucket o server externo."})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)