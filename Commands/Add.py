import os
from Singleton import Singleton

class Add():
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
            self.instancia.consola += "Error: La ruta o el archivo no existen.\n"
            self.instancia.escribirBitacora(f"Output - Add - Error: La ruta o el archivo no existen.")
            return

        try:
            # Abrir el archivo en modo anexar (append)
            with open(ruta_directorio, 'a') as archivo:
                # Agregar el texto nuevo al final del archivo
                archivo.write(self.body)

            print("Texto agregado al archivo correctamente.")
            self.instancia.escribirBitacora(f'Output - ADD - Texto agregado al archivo correctamente.')
            self.instancia.consola += "Texto agregado al archivo correctamente.\n"
        except IOError as e:
            print("Error al modificar el archivo:", str(e))
            self.instancia.escribirBitacora(f'Output - ADD - Error al modificar el archivo: {str(e)}')
            self.instancia.consola += f"Error al modificar el archivo: {str(e)}\n"
            return
        self.instancia.cLocal+=1

    
    def Cloud(self):
        pass