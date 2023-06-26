import os
from Singleton import Singleton
from pathlib import Path
import boto3

class Backup():
    def __init__(self,typeto, typefrom, ip, port, name) -> None:
        self.typeto=typeto
        self.typefrom=typefrom
        self.ip=ip
        self.port=port
        self.name=name
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.typefrom == "server":
            self.Local()
        elif self.typefrom == "bucket":
            self.Cloud()
    
    def Local(self):
        rutaorigen=Path("Archivos/")
        rutadestino="Archivos/"+self.name+"/"
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


            self.instancia.consola += f"Contenido de la carpeta copiado exitosamente a '{rutadestino}' del bucket\n"
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