import os
import shutil
from Singleton import Singleton

class Rename():
    def __init__(self, path, name) -> None:
        self.path = path
        self.name = name
        self.instancia = Singleton.getInstance()
        
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()
        ruta_directorio = ruta_directorio.replace('/', '\\')

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
        self.instancia.cLocal+=1

    
    def Cloud(self):
        pass