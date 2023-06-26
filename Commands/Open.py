import os
from Singleton import Singleton
import requests
import boto3

class Open():
    def __init__(self,type, ip, port, name) -> None:
        self.type=type
        self.ip=ip
        self.port=port
        self.name=name
        self.instancia = Singleton.getInstance()
        self.verificar = False
        
    def run(self):
        if self.ip != None and self.port != None:
            self.Api()
        elif self.type=="server":
            if self.verificar:
                return self.Local()
            self.Local()
        elif self.type=="bucket":
            if self.verificar:
                return self.Cloud()
            self.Cloud()
    
    def Local(self):
        ruta_archivo = os.path.join('Archivos', self.name)
        nombre = self.name.split("/")

        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                if self.verificar:
                    return contenido
                print(f"-> Este es el contenido del archivo {nombre[-1]}:\n {contenido}")
                self.instancia.consola += f"-----------------------------------------------------------------------------------\n"
                self.instancia.consola += f"-> Este es el contenido del archivo {nombre[-1]}:\n {contenido}\n"
                self.instancia.consola += f"-----------------------------------------------------------------------------------\n"
        else:
            if self.verificar:
                return f"ErrorOpen: No existe el archivo: {nombre[-1]}"
            print(f"Error, no existe el archivo: {nombre[-1]}")
            self.instancia.consola += f"Error, no existe el archivo: {nombre[-1]}\n"
    
    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta_archivo = carpeta + '/' + self.name
        nombre = ruta_archivo.split("/")
        
        contenido = self.obtener_contenido_archivo(s3, bucket_name, ruta_archivo)
        if contenido is not None:
            if self.verificar:
                return contenido
            print(f"-> Este es el contenido del archivo {nombre[-1]}:\n {contenido}")
            self.instancia.consola += "-----------------------------------------------------------------------------------\n"
            self.instancia.consola += f"-> Este es el contenido del archivo {nombre[-1]}:\n {contenido}\n"
            self.instancia.consola += "-----------------------------------------------------------------------------------\n"
        else:
            if self.verificar:
                return f"ErrorOpen: No existe el archivo: {nombre[-1]}"
            print(f"Error, no existe el archivo: {nombre[-1]}")
            self.instancia.consola += f"Error, no existe el archivo: {nombre[-1]}\n"

    def Api(self):
        url = f'http://{self.ip}:{self.port}/open'
        headers = {'Content-Type': 'application/json'}  # Especificamos el tipo de contenido del cuerpo
        
        data = {
            'type': self.type,
            'name': self.name
        }
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            texto = data['open']
            nombre = self.name.split("/")
            print(f"-> Este es el contenido del archivo {nombre[-1]}:\n {texto}")
            self.instancia.consola += f"-----------------------------------------------------------------------------------\n"
            self.instancia.consola += f"-> Este es el contenido del archivo {nombre[-1]}:\n {texto}\n"
            self.instancia.consola += f"-----------------------------------------------------------------------------------\n"
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