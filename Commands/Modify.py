import os
from Singleton import Singleton

class Modify():
    def __init__(self, path, body, type) -> None:
        self.path = path
        self.body = body
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

        # Verificar si la ruta y el archivo existen
        if not os.path.exists(ruta_directorio):
            print("Error: La ruta o el archivo no existen.")
             
            self.instancia.consola += "Error: La ruta o el archivo no existen.\n"
            return

        try:
            # Abrir el archivo en modo escritura
            with open(ruta_directorio, 'w') as archivo:
                # Escribir el texto nuevo en el archivo
                archivo.write(self.body)

            print("Archivo modificado correctamente.")
             
            self.instancia.consola += "Archivo modificado correctamente.\n"
        except IOError as e:
            print("Error al modificar el archivo:", str(e))
             
            self.instancia.consola += f"Error al modificar el archivo: {str(e)}\n"
            return

    
    def Cloud(self):
        pass
