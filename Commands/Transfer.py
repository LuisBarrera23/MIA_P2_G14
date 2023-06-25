import os
import shutil
from Singleton import Singleton
import boto3

class Transfer():
    def __init__(self, pfrom, pto, typeto, typefrom) -> None:
        self.pfrom = pfrom
        self.pto = pto
        self.typeto = typeto
        self.typefrom=typefrom
        self.instancia = Singleton.getInstance()

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
            
        # Validar la existencia del origen (ruta_directorio)
        if not os.path.exists(ruta_directorio):
            print(f"Error: El archivo o carpeta '{ruta_directorio}' no existe.")
             
            self.instancia.consola += f"Error: El archivo o carpeta '{ruta_directorio}' no existe.\n"
            return

        # Validar la existencia o creación del destino (ruta_destino)
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)
        
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

                            shutil.move(source_dir, destination_dir)                            

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

                            shutil.move(source_file, destination_file)
                        
                    cont += 1
                    if len(current_folder) > 0:
                        current_folder.pop(0)
                        
        else:
            # Transferir un archivo específico
            file_name = os.path.basename(ruta_directorio)
            destination_file = os.path.join(ruta_destino, file_name)
            if os.path.exists(destination_file):
                # Cambiar el nombre del archivo si ya existe en el destino
                base_name, extension = os.path.splitext(file_name)
                new_file = base_name + "_1" + extension
                destination_file = os.path.join(ruta_destino, new_file)
                print(f"Advertencia: El archivo '{file_name}' ya existe en el destino. Se guardará como '{new_file}'.")
                 
                self.instancia.consola += f"Advertencia: El archivo '{file_name}' ya existe en el destino. Se guardará como '{new_file}'.\n"
            shutil.move(ruta_directorio, destination_file)

        print("Transferencia completada.")
         
        self.instancia.consola += "Transferencia completada.\n"
    
    def Server_bucket(self):
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
                try:
                    os.makedirs(ruta_destino)
                    # print(f"Se ha creado la ruta de destino '{ruta_destino}'.")
                    # self.instancia.consola += f"Se ha creado la ruta de destino '{ruta_destino}'.\n"
                except OSError as e:
                    print(f"Error al crear la ruta de destino '{ruta_destino}': {e}")
                    self.instancia.consola += f"Error al crear la ruta de destino '{ruta_destino}': {e}\n"
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
                # s3.download_file(bucket_name, ruta_directorio, ruta_destino_archivo)
                # print(f"El archivo '{archivo}' se ha copiado correctamente.")
                # self.instancia.consola += f"El archivo '{archivo}' se ha copiado correctamente.\n"
                s3_resource = session.resource('s3')
                bucket = s3_resource.Bucket(bucket_name)
                s3_resource.Object(bucket_name, ruta_directorio).download_file(ruta_destino_archivo)
                s3.delete_object(Bucket=bucket_name, Key=ruta_directorio)
                print(f"El archivo '{archivo}' se ha transferido correctamente.")
                self.instancia.consola += f"El archivo '{archivo}' se ha transferido correctamente.\n"
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
                try:
                    os.makedirs(ruta_destino)
                    # print(f"Se ha creado la ruta de destino '{ruta_destino}'.")
                    # self.instancia.consola += f"Se ha creado la ruta de destino '{ruta_destino}'.\n"
                except OSError as e:
                    print(f"Error al crear la ruta de destino '{ruta_destino}': {e}")
                    self.instancia.consola += f"Error al crear la ruta de destino '{ruta_destino}': {e}\n"
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
                        # bucket.download_file(objeto.key, ruta_destino_objeto)
                        s3_resource.Object(bucket_name, ruta_objeto).download_file(ruta_destino_objeto)
                        s3.delete_object(Bucket=bucket_name, Key=ruta_objeto)
                    except s3.meta.client.exceptions.S3Exception as e:
                        print(f"Error, ocurrió un error al copiar el archivo '{ruta_relativa}': {e}")
                        self.instancia.consola += f"Error, ocurrió un error al copiar el archivo '{ruta_relativa}': {e}\n"
            self.instancia.consola += f"La carpeta '{ruta_directorio}' se ha transferido correctamente.\n"
            
            objects_to_delete = []
            result = s3.list_objects_v2(Bucket=bucket_name, Prefix=ruta_directorio)
            for obj in result.get('Contents', []):
                if obj['Key'] != carpeta:
                    objects_to_delete.append({'Key': obj['Key']})

            if objects_to_delete:
                s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
                # print("El contenido de la carpeta se ha vaciado correctamente.")
                # self.instancia.consola+="El contenido de la carpeta Archivos del bucket se ha vaciado correctamente.\n"
            else:
                print("La carpeta ya está vacía.")
                self.instancia.consola+="La carpeta ya está vacía.\n"
    
    def Cloud(self):
        pass