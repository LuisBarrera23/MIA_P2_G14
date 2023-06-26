import os
import shutil
from pathlib import Path
import boto3
from Singleton import Singleton

class Copy():
    def __init__(self, pfrom, pto , typeto, typefrom) -> None:
        self.pfrom = pfrom
        self.pto = pto
        self.typeto=typeto
        self.typefrom=typefrom
        self.instancia=Singleton.getInstance()
        
    def run(self):
        if self.typefrom == "server" and self.typeto=="server":
            self.Local()
        elif self.typefrom == "server" and self.typeto=="bucket":
            self.Server_bucket()
        elif self.typefrom == "bucket" and self.typeto=="server":
            self.Bucket_server()
        elif self.typefrom == "bucket" and self.typeto=="bucket":
            self.Cloud()
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.pfrom)
        ruta_directorio = ruta_directorio.rstrip()

        ruta_destino = os.path.join('Archivos', self.pto)
        ruta_destino = ruta_destino.rstrip()
        
        if ruta_directorio.endswith(".txt"):
            if os.path.isfile(ruta_directorio):
                if os.path.exists(ruta_destino) and os.path.isdir(ruta_destino):
                    nombre_archivo = os.path.basename(ruta_directorio)
                    nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
                    extension = os.path.splitext(nombre_archivo)[1]
                    ruta_destino_archivo = os.path.join(ruta_destino, nombre_archivo)
                    
                    # Verificar si el archivo ya existe en la ruta de destino
                    contador = 1
                    while os.path.exists(ruta_destino_archivo):
                        nombre_copia = f"{nombre_sin_extension}_copia{contador}{extension}"
                        ruta_destino_archivo = os.path.join(ruta_destino, nombre_copia)
                        contador += 1

                    # Realizar la copia del archivo
                    shutil.copy2(ruta_directorio, ruta_destino_archivo)
                    print("Archivo copiado exitosamente.")
                     
                    self.instancia.consola += "Archivo copiado exitosamente.\n"
                else:
                    print("Error: La carpeta de destino no existe.")
                     
                    self.instancia.consola += "Error: La carpeta de destino no existe.\n"
                    return
            else:
                print("Error: El archivo de origen no existe.")
                 
                self.instancia.consola += "Error: El archivo de origen no existe.\n"
                return
        else:
           
            if os.path.isdir(ruta_directorio):
                if os.path.exists(ruta_destino) and os.path.isdir(ruta_destino):
                    current_folder = []
                    cont = 0
                    for root, dirs, files in os.walk(ruta_directorio):
                        if cont == 0:
                            current_folder.append(os.path.relpath(root, ruta_directorio))
                                
                            for dir in dirs:
                                if cont == 0:
                                    current_folder.append("")
                                source_dir = os.path.join(root, dir)
                                destination_dir = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio), dir)
                                # Verificar si el directorio ya existe en la ruta de destino
                                contador = 1
                                nombre_carpeta = dir
                                current_folder[-1] = dir
                                # current_folder.append(dir)
                                while os.path.exists(destination_dir):
                                    nombre_copia = f"{nombre_carpeta}_copia{contador}"
                                    destination_dir = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio), nombre_copia)
                                    contador += 1
                                    current_folder[-1] = nombre_copia

                                shutil.copytree(source_dir, destination_dir)                            

                            for file in files:
                                source_file = os.path.join(root, file)
                                destination_dir = os.path.join(ruta_destino, current_folder[0])
                                # destination_dir = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio))
                                destination_file = os.path.join(destination_dir, file)

                                # Verificar si el archivo ya existe en la ruta de destino
                                contador = 1
                                nombre_archivo = file
                                while os.path.exists(destination_file):
                                    nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
                                    extension = os.path.splitext(nombre_archivo)[1]
                                    nombre_copia = f"{nombre_sin_extension}_copia{contador}{extension}"
                                    destination_file = os.path.join(destination_dir, nombre_copia)
                                    contador += 1

                                shutil.copy2(source_file, destination_file)
                            
                        cont += 1
                        if len(current_folder) > 0:
                            current_folder.pop(0)

                    print("Contenido de la carpeta copiado exitosamente.")
                     
                    self.instancia.consola += "Contenido de la carpeta copiado exitosamente.\n"
                else:
                    print("Error: La carpeta de destino no existe.")
                     
                    self.instancia.consola += "Error: La carpeta de destino no existe.\n"
                    return
            else:
                print("Error: La carpeta de origen no existe.")
                 
                self.instancia.consola += "Error: La carpeta de origen no existe.\n"
                return

    def Server_bucket(self):
        rutaorigen=Path("Archivos/"+self.pfrom)
        rutadestino="Archivos/"+self.pto
        if rutaorigen.exists():
            session = boto3.Session(
                aws_access_key_id=self.instancia.accesskey,
                aws_secret_access_key=self.instancia.secretaccesskey,
            )
            s3 = session.client('s3')
            if rutaorigen.is_file():
                if not self.file_or_folder_exists(s3,rutadestino):
                    self.instancia.consola += f"Error: La carpeta de destino no existe {rutadestino}\n"
                    return
                nombreArchivo=rutaorigen.name
                with open(rutaorigen, 'rb') as archivo:
                    nombreVerificado=nombreArchivo
                    nombreArchivo, extension = os.path.splitext(os.path.basename(rutaorigen))
                    i=1
                    while self.file_or_folder_exists(s3,rutadestino+"/"+nombreVerificado):
                        nombreVerificado = nombreArchivo+f"_{i}.{extension}"
                        i+=1

                    s3.upload_fileobj(archivo, 'proyecto2g14', rutadestino+"/"+nombreVerificado)
                    archivo.close()
                    self.instancia.consola += f"Archivo copiado exitosamente a '{rutadestino}' del bucket\n"
            elif rutaorigen.is_dir():
                # print(f"es una carpeta.")
                if not self.file_or_folder_exists(s3,rutadestino):
                    self.instancia.consola += f"Error: La carpeta de destino no existe {rutadestino}\n"
                    return
                
                i=0
                for root, dirs, files in os.walk(rutaorigen):
                    for file_name in files:
                        # print(file_name)
                        local_file_path = os.path.join(root, file_name)
                        relative_path = os.path.relpath(local_file_path, rutaorigen)
                        s3_file_path = os.path.join(rutadestino, relative_path).replace("\\", "/")
                        s3_file_path = s3_file_path.lstrip("/")
                        s3_file_path = os.path.dirname(s3_file_path)
                        nombreArchivo, extension = os.path.splitext(file_name)
                        nombreVerificado = nombreArchivo + extension
                        i = 1
                        while self.file_or_folder_exists(s3, s3_file_path + "/" + nombreVerificado):
                            nombreVerificado = f"{nombreArchivo}_{i}{extension}"
                            i += 1
                        s3.upload_file(local_file_path, 'proyecto2g14', s3_file_path + "/" + nombreVerificado)
                self.instancia.consola += f"Contenido de la carpeta copiado exitosamente a '{rutadestino}' del bucket\n"
        else:
            print(f"{rutaorigen} no existe en el sistema de archivos.")
            self.instancia.consola += f"Error: La carpeta o archivo de origen no existe {rutaorigen}\n"
        pass

    def Bucket_server(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta_directorio = carpeta + "/" + self.pfrom
        ruta_destino = carpeta + "/" + self.pto
        
        if ruta_directorio.endswith(".txt"):
            # Separar la ruta del nombre de archivo
            carpeta_s3, archivo = os.path.split(ruta_directorio)

            try:
                # Verificar si el archivo existe en S3
                s3.head_object(Bucket=bucket_name, Key=ruta_directorio)
            except s3.exceptions.ClientError as e:
                # Si ocurre un error, el archivo no existe
                if e.response['Error']['Code'] == '404':
                    print(f"El archivo '{archivo}' no existe en S3.")
                    self.instancia.consola += f"El archivo '{archivo}' no existe en S3.\n"
                else:
                    print(f"Ocurrió un error al verificar el archivo: {e}")
                    self.instancia.consola += f"Ocurrió un error al verificar el archivo: {e}\n"
                return

            if not os.path.exists(ruta_destino):
                print(f"La ruta de destino '{ruta_destino}' no existe.")
                self.instancia.consola += f"La ruta de destino '{ruta_destino}' no existe.\n"
                return

            # Copiar el archivo a la ruta de destino en tu máquina física
            try:
                ruta_destino_archivo = ruta_destino + '/' + archivo
                archivo_dividido = archivo.split(".")
                nombre_sin_extension = archivo_dividido[0]
                extension = archivo_dividido[1]
                # Verificar si el archivo ya existe en la ruta de destino
                contador = 1
                while os.path.exists(ruta_destino_archivo):
                    nombre_copia = f"{nombre_sin_extension}_copia{contador}.{extension}"
                    ruta_destino_archivo = ruta_destino + "/" + nombre_copia
                    contador += 1
                s3.download_file(bucket_name, ruta_directorio, ruta_destino_archivo)
                print(f"El archivo '{archivo}' se ha copiado correctamente.")
                self.instancia.consola += f"El archivo '{archivo}' se ha copiado correctamente.\n"
            except s3.exceptions.ClientError as e:
                print(f"Ocurrió un error al copiar el archivo: {e}")
                self.instancia.consola += f"Ocurrió un error al copiar el archivo: {e}\n"
        else:
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
                print(f"Error, la ruta de destino '{ruta_destino}' no existe.")
                self.instancia.consola += f"Error, la ruta de destino '{ruta_destino}' no existe.\n"
                return

            # Descargar todos los objetos dentro de la carpeta
            s3_resource = session.resource('s3')
            bucket = s3_resource.Bucket(bucket_name)

            for objeto in bucket.objects.filter(Prefix=ruta_directorio+'/'):
                # Obtener la ruta completa del objeto
                ruta_objeto = objeto.key

                # Obtener la ruta relativa del objeto dentro de la carpeta
                ruta_relativa = os.path.relpath(ruta_objeto, ruta_directorio)

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
            self.instancia.consola += f"La carpeta '{ruta_directorio}' se ha copiado correctamente.\n"

    def Cloud(self):#funcion para bucket bucket
        # Establecer conexión con AWS S3
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        s3 = session.client('s3')
        rutaorigen="Archivos/"+self.pfrom
        rutadestino="Archivos/"+self.pto+"/"
        if not self.file_or_folder_exists(s3,rutaorigen):
            self.instancia.consola += f"Error: La carpeta o archivo de origen no existe {rutaorigen}\n"
            return
        if not self.file_or_folder_exists(s3,rutadestino):
            self.instancia.consola += f"Error: La carpeta de destino no existe {rutadestino}\n"
            return
        if not ".txt" in self.pfrom:
            rutaorigen+="/"
            # Obtener una lista de todos los objetos en la carpeta de origen
            result = s3.list_objects(Bucket='proyecto2g14', Prefix=rutaorigen)

            # Copiar cada objeto de la carpeta de origen a la carpeta de destino
            for content in result.get("Contents", []):
                file_key = content.get("Key")
                archivoFuente = {
                    "Bucket": 'proyecto2g14',
                    "Key": file_key
                }
                RutaDestino = file_key.replace(rutaorigen, rutadestino)
                if ".txt" in RutaDestino:
                    nombre_archivo,extension = os.path.splitext(os.path.basename(RutaDestino))
                    ruta = os.path.dirname(RutaDestino)+"/"
                    i=1
                    while self.file_or_folder_exists(s3,RutaDestino):
                        RutaDestino = ruta + nombre_archivo+f"_{i}{extension}"
                        i+=1
                s3.copy(archivoFuente, 'proyecto2g14', RutaDestino)
            self.instancia.consola += f"La carpeta '{rutaorigen}' se ha copiado correctamente.\n"
        else:
            # Código para cuando es un archivo.txt
            nombre_archivo,extension = os.path.splitext(os.path.basename(rutaorigen))  # Obtener el nombre del archivo de la ruta de origen
            RutaDestino = rutadestino + nombre_archivo+extension
            
            i=1
            while self.file_or_folder_exists(s3,RutaDestino):
                RutaDestino = rutadestino + nombre_archivo+f"_{i}{extension}"
                i+=1
            archivoFuente = {"Bucket": 'proyecto2g14',"Key": rutaorigen}
            s3.copy_object(CopySource=archivoFuente,Bucket='proyecto2g14',Key=RutaDestino)
            self.instancia.consola += f"El Archivo '{rutaorigen}' se ha copiado correctamente.\n"


    def file_or_folder_exists(self, s3, path):
        response = s3.list_objects_v2(Bucket='proyecto2g14', Prefix=path)
        return 'Contents' in response
    