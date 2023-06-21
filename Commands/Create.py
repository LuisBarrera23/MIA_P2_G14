import os
from Singleton import Singleton

class Create():
    def __init__(self, name, body, path) -> None:
        self.name = name
        self.body = body
        self.path = path
        self.instancia = Singleton.getInstance()
        
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()
        ruta_directorio = ruta_directorio.replace('/', '\\')
        if not os.path.exists(ruta_directorio):
            # Si no existe, crear el directorio
            os.makedirs(ruta_directorio)
            print(f"Directorio '{ruta_directorio}' creado.")
             
            self.instancia.consola += f"Directorio '{ruta_directorio}' creado.\n"
            
        ruta_archivo = os.path.join(ruta_directorio, self.name)
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(self.body)
        archivo.close()
        self.instancia.cLocal+=1
    
    def Cloud(self):
        pass