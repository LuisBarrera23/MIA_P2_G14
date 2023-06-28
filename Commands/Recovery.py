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
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta_directorio = carpeta + "/" + self.name
        ruta_destino = carpeta
        
        # try:
        #     # Verificar si la carpeta existe en S3
        #     s3.head_object(Bucket=bucket_name, Key=ruta_directorio+'/')
        # except s3.exceptions.ClientError as e:
        #     # Si ocurre un error, la carpeta no existe
        #     if e.response['Error']['Code'] == '404':
        #         print(f"Error, la carpeta '{ruta_directorio}' no existe en S3.")
        #         self.instancia.consola += f"Error, la carpeta '{ruta_directorio}' no existe en S3.\n"
        #     else:
        #         print(f"Error, ocurrió un error al verificar la carpeta: {e}")
        #         self.instancia.consola += f"Error, ocurrió un error al verificar la carpeta: {e}\n"
        #     return
        
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=ruta_directorio+'/')
        if 'Contents' in response:
            pass
        else:
            print(f"Error, la ruta no existe: {ruta_directorio}")
            self.instancia.consola += f"Error, la ruta no existe: {ruta_directorio}\n"
            return

        # Descargar todos los objetos dentro de la carpeta
        s3_resource = session.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)

        for objeto in bucket.objects.filter(Prefix=ruta_directorio+'/'):
            # Obtener la ruta completa del objeto
            ruta_objeto = objeto.key
            # Obtener la ruta relativa del objeto dentro de la carpeta
            ruta_relativa = os.path.relpath(ruta_objeto, ruta_directorio)
            
            # print(f"{ruta_objeto} - {ruta_relativa}")

            # Construir la ruta de destino
            ruta_destino_objeto = os.path.join(ruta_destino, ruta_relativa)

            if objeto.key[-1] == '/':  # Es un directorio
                # Crear el directorio en la ruta de destino
                os.makedirs(ruta_destino_objeto, exist_ok=True)
            else:  # Es un archivo
                # Descargar el archivo en la ruta de destino
                try:
                    archivo_dividido = ruta_destino_objeto.split(".")
                    nombre_sin_extension = archivo_dividido[0]
                    extension = archivo_dividido[1]
                    # Verificar si el archivo ya existe en la ruta de destino
                    contador = 1
                    while os.path.exists(ruta_destino_objeto):
                        ruta_destino_objeto = f"{nombre_sin_extension}_copia{contador}.{extension}"
                        contador += 1
                    bucket.download_file(objeto.key, ruta_destino_objeto)
                except s3.meta.client.exceptions.S3Exception as e:
                    print(f"Error, ocurrió un error al copiar el archivo '{ruta_relativa}': {e}")
                    self.instancia.consola += f"Error, ocurrió un error al copiar el archivo '{ruta_relativa}': {e}\n"
        self.instancia.consola += f"Se ha realizado el recovery correctamente.\n"

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
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta_directorio = carpeta + "/" + self.name
        ruta_destino = carpeta
        
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=ruta_directorio+'/')
        if 'Contents' in response:
            pass
        else:
            print(f"Error, la ruta no existe: {ruta_directorio}")
            self.instancia.consola += f"Error, la ruta no existe: {ruta_directorio}\n"
            return {'Error':f"Error, la ruta no existe: {ruta_directorio}\n"}

        # Descargar todos los objetos dentro de la carpeta
        s3_resource = session.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        
        data = {
        }

        for objeto in bucket.objects.filter(Prefix=ruta_directorio+'/'):
            # Obtener la ruta completa del objeto
            ruta_objeto = objeto.key
            # Obtener la ruta relativa del objeto dentro de la carpeta
            ruta_relativa = os.path.relpath(ruta_objeto, ruta_directorio)
            
            # Construir la ruta de destino
            ruta_destino_objeto = os.path.join(ruta_destino, ruta_relativa)

            if objeto.key[-1] == '/':  # Es un directorio
                ruta_destino_objeto = ruta_destino_objeto.replace('\\\\', '/')
                ruta_destino_objeto = ruta_destino_objeto.replace('\\', '/')
                data[ruta_destino_objeto] = 'None'
            else:  # Es un archivo
                contenido = self.obtener_contenido_archivo(s3, bucket_name, ruta_objeto)
                if contenido is not None:
                    ruta_destino_objeto = ruta_destino_objeto.replace('\\\\', '/')
                    ruta_destino_objeto = ruta_destino_objeto.replace('\\', '/')
                    data[ruta_destino_objeto] = contenido
                else:
                    continue

        json_data = json.dumps(data)
        json_data = json_data.replace("\\\\","/")
        return json_data
    
    def obtener_contenido_archivo(self, s3, bucket_name, ruta_archivo):
        try:
            response = s3.get_object(Bucket=bucket_name, Key=ruta_archivo)
            contenido = response['Body'].read().decode('utf-8')
            return contenido
        except s3.exceptions.NoSuchKey:
            return None

    def toServer(self):
        url = f'http://{self.ip}:{self.port}/recovery'
        headers = {'Content-Type': 'application/json'}  # Especificamos el tipo de contenido del cuerpo
        
        data = {
            'type_from': self.typefrom,
            'name':self.name
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            data = json.loads(data)
            print(data)
            res = data['recovery']
            for (key, value) in res.items():
                if value == 'None':
                    os.makedirs(key, exist_ok=True)
                else:
                    with open(key, "w") as file:
                        file.write(value)
            self.instancia.consola += "El recovery del server externo se ha generado correctamente."
        else:
            print(f'Error en la comunicación con el backend con ip: {self.ip} y port: {self.port}.')
            self.instancia.consola += f'Error en la comunicación con el backend con ip: {self.ip} y port: {self.port}.\n'
    
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
            respuesta = json.loads(respuesta)
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

        