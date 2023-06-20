import os
from datetime import datetime
from login import Login


def bitacora():
    data = datetime.now()
    dia = data.day
    mes = data.month
    año = data.year
    ruta = f"./Archivos/{año}/{mes}/{dia}/"
    carpeta = os.path.dirname(ruta)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    if not os.path.isfile(ruta+"log_archivos.txt"):
        with open(ruta+"log_archivos.txt", "w") as file:
            pass
        file.close()

    pass



if __name__ == "__main__":
    bitacora()
    login_window = Login()
    login_window.run()