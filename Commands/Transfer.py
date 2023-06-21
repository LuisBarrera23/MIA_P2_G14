import os
import shutil
from Singleton import Singleton

class Transfer():
    def __init__(self, pfrom, pto, mode) -> None:
        self.pfrom = pfrom
        self.pto = pto
        self.mode = mode
        self.instancia = Singleton.getInstance()
        
    def Local(self):
        if str(self.mode).lower() !=  str(self.instancia.type).lower():
            print("El modo seleccionado no es igual al de la configuración.")
             
            self.instancia.consola += "El modo seleccionado no es igual al de la configuración.\n"
            return
        ruta_directorio = os.path.join('Archivos', self.pfrom)
        ruta_directorio = ruta_directorio.rstrip()
        ruta_directorio = ruta_directorio.replace('/', '\\')

        ruta_destino = os.path.join('Archivos', self.pto)
        ruta_destino = ruta_destino.rstrip()
        ruta_destino = ruta_destino.replace('/', '\\')
            
        # Validar la existencia del origen (ruta_directorio)
        if not os.path.exists(ruta_directorio):
            print(f"Error: El archivo o carpeta '{ruta_directorio}' no existe.")
             
            self.instancia.consola += f"Error: El archivo o carpeta '{ruta_directorio}' no existe.\n"
            return

        # Validar la existencia o creación del destino (ruta_destino)
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        # Validar si ruta_directorio es una carpeta
        # if os.path.isdir(ruta_directorio):
        #     # Transferir el contenido de la carpeta raíz
        #     for root, dirs, files in os.walk(ruta_directorio):
        #         for dir in dirs:
        #             source_dir = os.path.join(root, dir)
        #             destination_dir = os.path.join(ruta_destino, os.path.relpath(source_dir, ruta_directorio))
        #             if not os.path.exists(destination_dir):
        #                 os.makedirs(destination_dir)

        #         for file in files:
        #             source_file = os.path.join(root, file)
        #             destination_file = os.path.join(ruta_destino, os.path.relpath(source_file, ruta_directorio))
        #             shutil.move(source_file, destination_file)
                    
        #     # Eliminar subdirectorios vacíos en la carpeta de origen
        #     for root, dirs, files in os.walk(ruta_directorio, topdown=False):
        #         for dir in dirs:
        #             dir_path = os.path.join(root, dir)
        #             if len(os.listdir(dir_path)) == 0:
        #                 os.rmdir(dir_path)
        
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

                            # if not os.path.exists(str(destination_dir)):
                            #     os.makedirs(destination_dir)
                                # os.makedirs(destination_dir, exist_ok=True)
                            # print(source_dir)
                            # print(destination_dir)
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
    
    def Cloud(self):
        pass