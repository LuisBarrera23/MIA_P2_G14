import os
from Singleton import Singleton

class Create():
    def __init__(self, name, body, path, type) -> None:
        self.name = name
        self.body = body
        self.path = path
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
        if not os.path.exists(ruta_directorio):
            # Si no existe, crear el directorio
            os.makedirs(ruta_directorio)
            print(f"Directorio '{ruta_directorio}' creado.")
             
            self.instancia.consola += f"Directorio '{ruta_directorio}' creado.\n"
            
        ruta_archivo = os.path.join(ruta_directorio, self.name)
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(self.body)
        archivo.close()
    
    def Cloud(self):
        pass