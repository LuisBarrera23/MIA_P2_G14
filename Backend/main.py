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

@app.route('/recovery',methods=['POST'])
def Recovery():
    type=request.json['type_from']
    name=request.json['name']
    print(f"Esto es lo que trae el json: type={type}, name={name}")
    return jsonify({
        "recovery": {
            "Archivos/carpeta 2": "None",
            "Archivos/carpeta 2/prueba 1": "None",
            "Archivos/carpeta 2/prueba 1/prueba2.txt": "Este es el contenido del archivo de la carpeta 2",
            "Archivos/carpeta 2/prueba 1/pureba": "None",
            "Archivos/carpeta 2/prueba 1/pureba/otra": "None",
            "Archivos/carpeta 2/prueba 1/pureba/otra/prueba 3.txt": "Este es el contenido del archivo del archivo 3",
            "Archivos/carpeta1": "None",
            "Archivos/carpeta1/prueba": "None",
            "Archivos/carpeta1/prueba/prueba1.txt": "File1",
            "Archivos/carpeta1/prueba4.txt": "File4",
            "Archivos/carpeta3": "None"
        }
    })

@app.route('/backup',methods=['POST'])
def Backup():
    print(request.get_json())
    return jsonify({'backup':"El backup se ha realizado correctamente."})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)