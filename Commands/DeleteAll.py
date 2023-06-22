import os
from Singleton import Singleton
import shutil
import boto3

class DeleteAll():
    def __init__(self,type) -> None:
        self.type=type
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.type=="server":
            self.Local()
        elif self.type=="bucket":
            self.Cloud()
    
    def Local(self):
        ruta="Archivos"
        for archivo in os.listdir(ruta):
            archivo_path = os.path.join(ruta, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)
            elif os.path.isdir(archivo_path):
                shutil.rmtree(archivo_path)
        print("La carpeta se ha vaciado correctamente.")
    
    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        ) 
        carpeta = 'Archivos'
        s3 = session.resource('s3')
        bucket = s3.Bucket('proyecto2g14' )

        objects_to_delete = []
        for obj in bucket.objects.filter(Prefix=carpeta):
            if obj.key != carpeta:
                objects_to_delete.append({'Key': obj.key})

        if objects_to_delete:
            bucket.delete_objects(Delete={'Objects': objects_to_delete})
            print("El contenido de la carpeta se ha vaciado correctamente.")
        else:
            print("La carpeta ya está vacía.")