import os
from Singleton import Singleton
import boto3

class Modify():
    def __init__(self, path, body, type) -> None:
        self.path = path
        self.body = body
        self.type = type
        self.instancia = Singleton.getInstance()
    
    def run(self):
        if self.type=="server":
            self.Local()
        elif self.type=="bucket":
            self.Cloud()

    
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()

        # Verificar si la ruta y el archivo existen
        if not os.path.exists(ruta_directorio):
            print("Error: La ruta o el archivo no existen.")
             
            self.instancia.consola += "Error: La ruta o el archivo no existen.\n"
            return

        try:
            # Abrir el archivo en modo escritura
            with open(ruta_directorio, 'w') as archivo:
                # Escribir el texto nuevo en el archivo
                archivo.write(self.body)

            print("Archivo modificado correctamente.")
             
            self.instancia.consola += "Archivo modificado correctamente.\n"
        except IOError as e:
            print("Error al modificar el archivo:", str(e))
             
            self.instancia.consola += f"Error al modificar el archivo: {str(e)}\n"
            return

    
    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        ruta = "Archivos/" + self.path
        print(ruta)
        s3 = session.resource('s3')
        response = s3.meta.client.list_objects_v2(Bucket='proyecto2g14', Prefix=ruta)

        if 'Contents' in response:
            print(f"La ruta existe: {ruta}")
            print("-------------------------------------")
            obj = s3.Object('proyecto2g14', ruta)
            obj.put(Body=self.body)
            self.instancia.consola += f"Archivo modificado correctamente para el archivo: {ruta}\n"
        else:
            print(f"Error, la ruta o archivo no existe: {ruta}")
            self.instancia.consola += f"Error, la ruta o archivo no existe: {ruta}\n"
            return
