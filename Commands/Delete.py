import os
import shutil
from Singleton import Singleton

class Delete():
    def __init__(self, path, name) -> None:
        self.path = path
        self.name = name
        self.instancia = Singleton.getInstance()
        
    def Local(self):
        # Validar si el path existe
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()
        ruta_directorio = ruta_directorio.replace('/', '\\')
        if os.path.exists(ruta_directorio):
            print(f"La ruta existe: {self.path}")
            print("-------------------------------------")
        else:
            print(f"La ruta no existe: {self.path}")
            self.instancia.consola += f"La ruta no existe: {self.path}\n"
            self.instancia.escribirBitacora(f'Output - Delete - La ruta no existe: {self.path}')
            return
        
        # Eliminar carpetas o archivos
        if self.name is not None:
            ruta_directorio = os.path.join('Archivos', self.path)
            ruta_directorio = ruta_directorio.rstrip()
            ruta_directorio = ruta_directorio.replace('/', '\\')
            ruta_archivo = os.path.join(ruta_directorio, self.name)
                
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"Se eliminó el archivo '{os.path.basename(ruta_archivo)}' de la ruta '{ruta_archivo}'.")
                self.instancia.escribirBitacora(f'Output - Delete - Datos Correctos')
                self.instancia.consola += f"Se eliminó el archivo '{os.path.basename(ruta_archivo)}' de la ruta '{ruta_archivo}'.\n"
                print("-------------------------------------")
            else:
                print(f"El archivo '{os.path.basename(ruta_archivo)}' no existe en la ruta '{ruta_archivo}'.")
                self.instancia.escribirBitacora(f"Output - Delete - El archivo '{os.path.basename(ruta_archivo)}' no existe en la ruta '{ruta_archivo}'.")
                self.instancia.consola += f"El archivo '{os.path.basename(ruta_archivo)}' no existe en la ruta '{ruta_archivo}'.\n"
                return
        else:
            ruta_directorio = os.path.join('Archivos', self.path)
            ruta_directorio = ruta_directorio.rstrip()
            ruta_directorio = ruta_directorio.replace('/', '\\')
            
            ultima_carpeta = os.path.basename(ruta_directorio)
            if os.path.exists(ruta_directorio) and os.path.isdir(ruta_directorio):
                shutil.rmtree(ruta_directorio)
                print(f"Se eliminó la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.")
                self.instancia.escribirBitacora(f"Output - Delete - Se eliminó la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.")
                self.instancia.consola += f"Se eliminó la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.\n"
            else:
                print(f"No se pudo eliminar la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.")
                self.instancia.escribirBitacora(f'Output - Delete - No se pudo eliminar la carpeta "{ultima_carpeta}" de la ruta "{ruta_directorio}".')
                self.instancia.consola += f"No se pudo eliminar la carpeta '{ultima_carpeta}' de la ruta '{ruta_directorio}'.\n"
                return
        self.instancia.cLocal+=1
    
    def Cloud(self):
        pass