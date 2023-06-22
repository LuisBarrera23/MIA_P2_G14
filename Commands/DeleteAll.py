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
        self.instancia.consola+="El contenido de la carpeta Archivos del server se ha vaciado correctamente.\n"
    
    import boto3

    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos/'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'

        objects_to_delete = []
        result = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta)
        for obj in result.get('Contents', []):
            if obj['Key'] != carpeta:
                objects_to_delete.append({'Key': obj['Key']})

        if objects_to_delete:
            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
            print("El contenido de la carpeta se ha vaciado correctamente.")
            self.instancia.consola+="El contenido de la carpeta Archivos del bucket se ha vaciado correctamente.\n"
        else:
            print("La carpeta ya está vacía.")
            self.instancia.consola+="La carpeta ya está vacía.\n"