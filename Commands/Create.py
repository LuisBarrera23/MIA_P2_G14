import os
from Singleton import Singleton
import boto3

class Create():
    def __init__(self, name, body, path, type) -> None:
        self.name = name
        self.body = body
        self.path = path
        self.type = type
        self.instancia = Singleton.getInstance()
        # print(f"{self.name}, {self.body}, {self.path}, {self.type}")
        

    def run(self):
        if self.type=="server":
            self.Local()
        elif self.type=="bucket":
            self.Cloud()
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()
        if not os.path.exists(ruta_directorio):
            # Si no existe, crear el directorio
            os.makedirs(ruta_directorio)
            print(f"Directorio '{ruta_directorio}' creado.")
             
            self.instancia.consola += f"Directorio '{ruta_directorio}' creado.\n"
            
        ruta_archivo = os.path.join(ruta_directorio, self.name)
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(self.body)
        archivo.close()
    
    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        # Dividimos la ruta en diferentes partes para crear las carpetas anidadas
        folders = self.path.split('/')
        folder_path = carpeta
        
        for folder in folders:
            folder_path += '/' + folder
            
            # Comprobamos si la carpeta actual existe, si no existe, la creamos
            if not self.folder_exists(s3, folder_path):
                self.create_folder(s3, folder_path)
        
        # Creamos el archivo en la ubicación especificada
        file_path = folder_path + '/' + self.name
        s3.put_object(Body=self.body, Bucket=bucket_name, Key=file_path)
        
        print(f"Archivo {self.name} creado en la ruta {file_path}")
        self.instancia.consola += f"Archivo {self.name} creado en la ruta {file_path}.\n"
        
    def folder_exists(self, s3, folder_path):
        response = s3.list_objects_v2(Bucket='proyecto2g14', Prefix=folder_path)
        return 'Contents' in response

    def create_folder(self, s3, folder_path):
        s3.put_object(Body='', Bucket='proyecto2g14', Key=(folder_path + '/'))