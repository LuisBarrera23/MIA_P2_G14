import os
import shutil
from Singleton import Singleton
import boto3

class Rename():
    def __init__(self, path, name, type) -> None:
        self.path = path
        self.name = name
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

        # Verificar si el archivo o carpeta existe
        if not os.path.exists(ruta_directorio):
            print(f"Error: No existe el archivo o carpeta '{self.path}'")
             
            self.instancia.consola += f"Error: No existe el archivo o carpeta '{self.path}'\n"
            return
        
        new_path = os.path.join(os.path.dirname(ruta_directorio), self.name)
        
        # Verificar si ya existe un archivo o carpeta con el nuevo nombre
        if os.path.exists(new_path):
            print(f"Error: Ya existe un archivo o carpeta con el nombre '{self.name}'")
             
            self.instancia.consola += f"Error: Ya existe un archivo o carpeta con el nombre '{self.name}'\n"
            return
        
        try:
            # Renombrar el archivo o carpeta
            os.rename(ruta_directorio, new_path)
            print(f"¡Renombrado exitosamente a '{self.name}'!")
             
            self.instancia.consola += f"¡Renombrado exitosamente a '{self.name}'!\n"
        except Exception as e:
            print(f"Error al renombrar: {e}")
             
            self.instancia.consola += f"Error al renombrar: {e}\n"
            return

    
    def Cloud(self):
        session = boto3.Session(
            aws_access_key_id=self.instancia.accesskey,
            aws_secret_access_key=self.instancia.secretaccesskey,
        )
        carpeta = 'Archivos'
        s3 = session.client('s3')
        bucket_name = 'proyecto2g14'
        
        ruta = "Archivos/"+self.path
        # Verificamos si el archivo o carpeta existe
        if not self.file_or_folder_exists(s3, ruta):
            print(f"Error, el archivo o carpeta '{ruta}' no existe.")
            self.instancia.consola += f"Error, el archivo o carpeta '{ruta}' no existe.\n"
            return
        
        # Obtenemos el nombre del archivo o carpeta actual
        current_name = self.get_file_or_folder_name(ruta)
        
        # Obtenemos la ruta del directorio actual
        directory_path = self.get_directory_path(ruta)
        
        # Comprobamos si ya existe un archivo o carpeta con el nombre deseado en el directorio actual
        if self.file_or_folder_exists(s3, directory_path + '/' + self.name):
            print(f"Error, ya existe un archivo o carpeta llamado '{self.name}' en el directorio actual.")
            self.instancia.consola += f"Error, ya existe un archivo o carpeta llamado '{self.name}' en el directorio actual.\n"
            return
        
        # Renombramos el archivo o carpeta
        new_path = directory_path + '/' + self.name
        
        if '.txt' in self.path:
            s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': ruta}, Key=new_path)
            s3.delete_object(Bucket=bucket_name, Key=ruta)
        else:
            ruta += '/'
            new_path += '/'
            # Obtener la lista de objetos en la carpeta original
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=ruta)

            # Copiar cada objeto a la nueva carpeta con el nuevo nombre
            for obj in response['Contents']:
                old_key = obj['Key']
                new_key = old_key.replace(ruta, new_path, 1)
                
                s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': old_key}, Key=new_key)
                s3.delete_object(Bucket=bucket_name, Key=old_key)
        
        print(f"Archivo o carpeta '{current_name}' renombrado como '{self.name}' en la ruta '{new_path}'")
        self.instancia.consola += f"Archivo o carpeta '{current_name}' renombrado como '{self.name}' en la ruta '{new_path}'\n"
        
    def file_or_folder_exists(self, s3, path):
        response = s3.list_objects_v2(Bucket='proyecto2g14', Prefix=path)
        return 'Contents' in response

    def get_file_or_folder_name(self, path):
        return path.split('/')[-1]

    def get_directory_path(self, path):
        return '/'.join(path.split('/')[:-1])