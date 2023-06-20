import os
from Singleton import Singleton

class Modify():
    def __init__(self, path, body) -> None:
        self.path = path
        self.body = body
        self.instancia = Singleton.getInstance()
        
    def Local(self):
        ruta_directorio = os.path.join('Archivos', self.path)
        ruta_directorio = ruta_directorio.rstrip()
        ruta_directorio = ruta_directorio.replace('/', '\\')

        # Verificar si la ruta y el archivo existen
        if not os.path.exists(ruta_directorio):
            print("Error: La ruta o el archivo no existen.")
            self.instancia.escribirBitacora(f'Output - Modify - Error: La ruta o el archivo no existen.')
            self.instancia.consola += "Error: La ruta o el archivo no existen.\n"
            return

        try:
            # Abrir el archivo en modo escritura
            with open(ruta_directorio, 'w') as archivo:
                # Escribir el texto nuevo en el archivo
                archivo.write(self.body)

            print("Archivo modificado correctamente.")
            self.instancia.escribirBitacora(f'Output - Modify - Archivo modificado correctamente.')
            self.instancia.consola += "Archivo modificado correctamente.\n"
        except IOError as e:
            print("Error al modificar el archivo:", str(e))
            self.instancia.escribirBitacora(f'Output - Modify - Error al modificar el archivo')
            self.instancia.consola += f"Error al modificar el archivo: {str(e)}\n"
            return
        self.instancia.cLocal+=1

    
    def Cloud(self):
        pass
