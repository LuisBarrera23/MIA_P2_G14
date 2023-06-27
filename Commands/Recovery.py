import os
from Singleton import Singleton
from pathlib import Path
import json
import boto3
import requests

class Recovery():
    def __init__(self,typeto, typefrom, ip, port, name) -> None:
        self.typeto=typeto
        self.typefrom=typefrom
        self.ip=ip
        self.port=port
        self.name=name
        self.consulta=False
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.consulta:
            if self.typefrom == "server":
                return self.fromServer()
            elif self.typefrom == "bucket":
                return self.fromBucket()
        elif self.ip != None and self.port != None:
            if self.typeto == "server":
                self.toServer()
            elif self.typeto == "bucket":
                self.toBucket()
        elif self.typefrom == "server" and self.typeto == "bucket":
            self.Local()
        elif self.typefrom == "bucket" and self.typeto == "server":
            self.Cloud()
    
    def Local(self):
        rutaorigen=Path("Archivos/"+self.name)
        rutadestino="Archivos/"
        if rutaorigen.exists():
            session = boto3.Session(
                aws_access_key_id=self.instancia.accesskey,
                aws_secret_access_key=self.instancia.secretaccesskey,
            )
            s3 = session.client('s3')
            
            for root, dirs, files in os.walk(rutaorigen, topdown=False):
                for file_name in files:
                    local_file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(local_file_path, rutaorigen)
                    s3_file_path = os.path.join(rutadestino, relative_path).replace("\\", "/")
                    s3_file_path = s3_file_path.lstrip("/")
                    s3_file_path = os.path.dirname(s3_file_path)
                    s3.upload_file(local_file_path, 'proyecto2g14', s3_file_path + "/" + file_name)

            for root, dirs, _ in os.walk(rutaorigen):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    relative_path = os.path.relpath(dir_path, rutaorigen)
                    s3_dir_path = os.path.join(rutadestino, relative_path).replace("\\", "/")
                    s3_dir_path = s3_dir_path.lstrip("/")
                    
                    try:
                        s3.head_object(Bucket='proyecto2g14', Key=s3_dir_path + "/")
                    except:
                        s3.put_object(Body="", Bucket='proyecto2g14', Key=s3_dir_path + "/")


            self.instancia.consola += f"Recovery restaurado exitosamente a '{rutadestino}' del bucket\n"
        else:
            print(f"{rutaorigen} no existe en el sistema de archivos.")
            self.instancia.consola += f"Error: La carpeta o archivo de origen no existe {rutaorigen}\n"
    
    def Cloud(self):
        pass

    def fromServer(self):
        rutaorigen = Path("Archivos/"+self.name)
        
        if rutaorigen.exists():
            data = {}
            
            for root, dirs, files in os.walk(rutaorigen):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    relative_path = os.path.relpath(dir_path, rutaorigen)
                    data[f"Archivos/"+relative_path] = "None"
                
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, rutaorigen)
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    data[f"Archivos/"+relative_path] = file_content
            
            json_data = json.dumps(data)
            json_data = json_data.replace("\\\\","/")
            # print(json_data)
            return json_data
        else:
            print(f"{rutaorigen} no existe en el sistema de archivos.")
            return "{}"     

    def fromBucket(self):
        pass

    def toServer(self):
        pass
    
    def toBucket(self):
        url = f'http://{self.ip}:{self.port}/recovery'
        headers = {'Content-Type': 'application/json'}
        json_data={"type_from":self.typefrom,"name": self.name}
        response = requests.post(url, json=json_data, headers=headers)
        respuesta=""
        data=""
        # Aquí puedes hacer lo que necesites con el JSON generado, como guardarlo en un archivo
        if response.status_code == 200:
            respuesta = response.json()
            data = json.loads(respuesta['recovery'])
            # data = respuesta['recovery']
            print(data)
        else:
            print(f'Error en la comunicación con el backend con ip: {self.ip} y port: {self.port}.')
            self.instancia.consola += f'Error en la comunicación con el backend con ip: {self.ip} y port: {self.port}.\n'
            return

        # Crear las carpetas y archivos en S3
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        s3 = session.client('s3')

        for key, value in data.items():
            if value == "None":
                # Crear carpeta en S3
                if "." != key[-1]:
                    s3.put_object(Bucket='proyecto2g14', Key=key + "/")
            else:
                # Crear archivo en S3 con el contenido
                s3.put_object(Bucket='proyecto2g14', Key=key, Body=value.encode())

        return "El Backup enviado se ha guardado correctamente en el Bucket externo."

        