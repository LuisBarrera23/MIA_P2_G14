import os
from Singleton import Singleton
import boto3
import requests

class Backup():
    def __init__(self,typeto, typefrom, ip, port, name) -> None:
        self.typeto=typeto
        self.typefrom=typefrom
        self.ip=ip
        self.port=port
        self.name=name
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.ip != None and self.port != None:
            if self.typefrom == "bucket":
                self.fromBucket()
            elif self.typefrom == "server":
                self.fromServer()
        elif self.typefrom == "server" and self.typeto == "bucket":
            self.Local()
        elif self.typefrom == "bucket" and self.typeto == "server":
            self.Cloud()
    
    def Local(self):
        pass
    
    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta_directorio = carpeta
        ruta_destino = carpeta + "/" + self.name
        
        try:
            # Verificar si la carpeta existe en S3
            s3.head_object(Bucket=bucket_name, Key=ruta_directorio+'/')
        except s3.exceptions.ClientError as e:
            # Si ocurre un error, la carpeta no existe
            if e.response['Error']['Code'] == '404':
                print(f"Error, la carpeta '{ruta_directorio}' no existe en S3.")
                self.instancia.consola += f"Error, la carpeta '{ruta_directorio}' no existe en S3.\n"
            else:
                print(f"Error, ocurrió un error al verificar la carpeta: {e}")
                self.instancia.consola += f"Error, ocurrió un error al verificar la carpeta: {e}\n"
            return

        if not os.path.exists(ruta_destino):
            try:
                os.makedirs(ruta_destino)
            except OSError as e:
                print(f"Error al crear la ruta de destino '{ruta_destino}': {e}")
                self.instancia.consola += f"Error al crear la ruta de destino '{ruta_destino}': {e}\n"
                return

        # Descargar todos los objetos dentro de la carpeta
        s3_resource = session.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)

        # print("================================================================================================")
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
        # print("================================================================================================")
        self.instancia.consola += f"Se ha realizado el backup correctamente en la carpeta: {self.name}.\n"
        
    def fromBucket(self):
        url = f'http://{self.ip}:{self.port}/backup'
        headers = {'Content-Type': 'application/json'}  # Especificamos el tipo de contenido del cuerpo
        
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta_directorio = carpeta
        ruta_destino = carpeta + "/" + self.name
        
        try:
            # Verificar si la carpeta existe en S3
            s3.head_object(Bucket=bucket_name, Key=ruta_directorio+'/')
        except s3.exceptions.ClientError as e:
            # Si ocurre un error, la carpeta no existe
            if e.response['Error']['Code'] == '404':
                print(f"Error, la carpeta '{ruta_directorio}' no existe en S3.")
                self.instancia.consola += f"Error, la carpeta '{ruta_directorio}' no existe en S3.\n"
            else:
                print(f"Error, ocurrió un error al verificar la carpeta: {e}")
                self.instancia.consola += f"Error, ocurrió un error al verificar la carpeta: {e}\n"
            return

        # Descargar todos los objetos dentro de la carpeta
        s3_resource = session.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        
        data = {
            'type_to': self.typeto,
        }

        for objeto in bucket.objects.filter(Prefix=ruta_directorio+'/'):
            # Obtener la ruta completa del objeto
            ruta_objeto = objeto.key
            # Obtener la ruta relativa del objeto dentro de la carpeta
            ruta_relativa = os.path.relpath(ruta_objeto, ruta_directorio)
            
            # Construir la ruta de destino
            ruta_destino_objeto = os.path.join(ruta_destino, ruta_relativa)

            if objeto.key[-1] == '/':  # Es un directorio
                data[ruta_destino_objeto] = 'None'
            else:  # Es un archivo
                contenido = self.obtener_contenido_archivo(s3, bucket_name, ruta_objeto)
                if contenido is not None:
                    data[ruta_destino_objeto] = contenido
                else:
                    continue

        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            res = data['backup']
            print(res)
            self.instancia.consola += f"{res}"
        else:
            print(f'Error en la comunicación con el backend con ip: {self.ip} y port: {self.port}.')
            self.instancia.consola += f'Error en la comunicación con el backend con ip: {self.ip} y port: {self.port}.\n'
            
    def obtener_contenido_archivo(self, s3, bucket_name, ruta_archivo):
        try:
            response = s3.get_object(Bucket=bucket_name, Key=ruta_archivo)
            contenido = response['Body'].read().decode('utf-8')
            return contenido
        except s3.exceptions.NoSuchKey:
            return None

    def fromServer(self):
        pass