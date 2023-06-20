import os
import shutil
from Singleton import Singleton

class Copy():
    def __init__(self, pfrom, pto) -> None:
        self.pfrom = pfrom
        self.pto = pto
        self.instancia=Singleton.getInstance()
        
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.pfrom)
        ruta_directorio = ruta_directorio.rstrip()
        ruta_directorio = ruta_directorio.replace('/', '\\')

        ruta_destino = os.path.join('Archivos', self.pto)
        ruta_destino = ruta_destino.rstrip()
        ruta_destino = ruta_destino.replace('/', '\\')
        
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
                    self.instancia.escribirBitacora(f'Output - Copy - Archivo copiado exitosamente.')
                    self.instancia.consola += "Archivo copiado exitosamente.\n"
                else:
                    print("Error: La carpeta de destino no existe.")
                    self.instancia.escribirBitacora(f'Output - Copy - Error: La carpeta de destino no existe.')
                    self.instancia.consola += "Error: La carpeta de destino no existe.\n"
                    return
            else:
                print("Error: El archivo de origen no existe.")
                self.instancia.escribirBitacora(f'Output - Copy - Error: El archivo de origen no existe.')
                self.instancia.consola += "Error: El archivo de origen no existe.\n"
                return
        else:
            # if os.path.isdir(ruta_directorio):
            #     if os.path.exists(ruta_destino) and os.path.isdir(ruta_destino):
            #         for root, dirs, files in os.walk(ruta_directorio):
            #             for dir in dirs:
            #                 source_dir = os.path.join(root, dir)
            #                 destination_dir = os.path.join(ruta_destino, os.path.relpath(source_dir, ruta_directorio))
            #                 os.makedirs(destination_dir, exist_ok=True)

            #             for file in files:
            #                 source_file = os.path.join(root, file)
            #                 destination_file = os.path.join(ruta_destino, os.path.relpath(source_file, ruta_directorio))
            #                 shutil.copy2(source_file, destination_file)

            #         print("Contenido de la carpeta copiado exitosamente.")
            #         self.instancia.escribirBitacora(f'Output - Copy - Contenido de la carpeta copiado exitosamente.')
            #         self.instancia.consola += "Contenido de la carpeta copiado exitosamente.\n"
            
            
            # if os.path.isdir(ruta_directorio):
            #     if os.path.exists(ruta_destino) and os.path.isdir(ruta_destino):
            #         for root, dirs, files in os.walk(ruta_directorio):
            #             for dir in dirs:
            #                 source_dir = os.path.join(root, dir)
            #                 destination_dir = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio), dir)

            #                 # Verificar si el directorio ya existe en la ruta de destino
            #                 contador = 1
            #                 nombre_carpeta = dir
            #                 while os.path.exists(destination_dir):
            #                     nombre_copia = f"{nombre_carpeta}_copia{contador}"
            #                     destination_dir = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio), nombre_copia)
            #                     contador += 1

            #                 os.makedirs(destination_dir, exist_ok=True)

            #             for file in files:
            #                 source_file = os.path.join(root, file)
            #                 destination_file = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio), file)

            #                 # Verificar si el archivo ya existe en la ruta de destino
            #                 contador = 1
            #                 nombre_archivo = file
            #                 while os.path.exists(destination_file):
            #                     nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
            #                     extension = os.path.splitext(nombre_archivo)[1]
            #                     nombre_copia = f"{nombre_sin_extension}_copia{contador}{extension}"
            #                     destination_file = os.path.join(ruta_destino, os.path.relpath(root, ruta_directorio), nombre_copia)
            #                     contador += 1

            #                 shutil.copy2(source_file, destination_file)

            #         print("Contenido de la carpeta copiado exitosamente.")
            #         self.instancia.escribirBitacora(f'Output - Copy - Contenido de la carpeta copiado exitosamente.')
            #         self.instancia.consola += "Contenido de la carpeta copiado exitosamente.\n"
            
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
                    self.instancia.escribirBitacora('Output - Copy - Contenido de la carpeta copiado exitosamente.')
                    self.instancia.consola += "Contenido de la carpeta copiado exitosamente.\n"
                else:
                    print("Error: La carpeta de destino no existe.")
                    self.instancia.escribirBitacora(f'Output - Copy - Error: La carpeta de destino no existe.')
                    self.instancia.consola += "Error: La carpeta de destino no existe.\n"
                    return
            else:
                print("Error: La carpeta de origen no existe.")
                self.instancia.escribirBitacora(f'Output - Copy - Error: La carpeta de origen no existe.')
                self.instancia.consola += "Error: La carpeta de origen no existe.\n"
                return

        self.instancia.cLocal+=1
    
    def Cloud(self):
        pass