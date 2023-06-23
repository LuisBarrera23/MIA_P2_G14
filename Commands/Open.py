import os
from Singleton import Singleton
import requests

class Open():
    def __init__(self,type, ip, port, name) -> None:
        self.type=type
        self.ip=ip
        self.port=port
        self.name=name
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.ip != None and self.port != None:
            self.Api()
        elif self.type=="server":
            self.Local()
        elif self.type=="bucket":
            self.Cloud()
    
    def Local(self):
        ruta_archivo = os.path.join('Archivos', self.name)
        nombre = self.name.split("/")

        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                print(f"-> Este es el contenido del archivo {nombre[-1]}:\n {contenido}")
                self.instancia.consola += f"-----------------------------------------------------------------------------------\n"
                self.instancia.consola += f"-> Este es el contenido del archivo {nombre[-1]}:\n {contenido}\n"
                self.instancia.consola += f"-----------------------------------------------------------------------------------\n"
        else:
            print(f"Error, no existe el archivo: {nombre[-1]}")
            self.instancia.consola += f"Error, no existe el archivo: {nombre[-1]}\n"
    
    def Cloud(self):
        pass

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