import os
import shutil
from Singleton import Singleton

class Delete():
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
        # Validar si el path existe
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()
        if os.path.exists(ruta_directorio):
            print(f"La ruta existe: {self.path}")
            print("-------------------------------------")
        else:
            print(f"La ruta no existe: {self.path}")
            self.instancia.consola += f"La ruta no existe: {self.path}\n"
             
            return
        
        # Eliminar carpetas o archivos
        if self.name is not None:
            ruta_directorio = os.path.join('Archivos', self.path)
            ruta_directorio = ruta_directorio.rstrip()
            ruta_archivo = os.path.join(ruta_directorio, self.name)
                
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"Se eliminó el archivo '{os.path.basename(ruta_archivo)}' de la ruta '{ruta_archivo}'.")
                 
                self.instancia.consola += f"Se eliminó el archivo '{os.path.basename(ruta_archivo)}' de la ruta '{ruta_archivo}'.\n"
                print("-------------------------------------")
            else:
                print(f"El archivo '{os.path.basename(ruta_archivo)}' no existe en la ruta '{ruta_archivo}'.")
                 
                self.instancia.consola += f"El archivo '{os.path.basename(ruta_archivo)}' no existe en la ruta '{ruta_archivo}'.\n"
                return
        else:
            ruta_directorio = os.path.join('Archivos', self.path)
            ruta_directorio = ruta_directorio.rstrip()
            
            ultima_carpeta = os.path.basename(ruta_directorio)
            if os.path.exists(ruta_directorio) and os.path.isdir(ruta_directorio):
                shutil.rmtree(ruta_directorio)
                print(f"Se eliminó la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.")
                 
                self.instancia.consola += f"Se eliminó la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.\n"
            else:
                print(f"No se pudo eliminar la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.")
                 
                self.instancia.consola += f"No se pudo eliminar la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.\n"
                return
    
    def Cloud(self):
        pass