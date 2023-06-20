from window import MainWindow
from Singleton import Singleton

import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import binascii
import os
from datetime import datetime

class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inicio de sesión")
        self.instancia=Singleton.getInstance()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        ancho = 400
        largo = 250
        self.root.geometry(f"{int(ancho)}x{int(largo)}")  #tamaño de la ventana
         # Calcular la posición de la ventana
        x = (screen_width / 2) - (ancho / 2) 
        y = (screen_height / 2) - (largo / 2)  

        # Mover la ventana a la posición calculada
        self.root.geometry(f"+{int(x)}+{int(y)}")
        self.root.config(bg="#4287f5")  # color de fondo de la ventana

        # Crear los campos de entrada
        label_username = tk.Label(self.root, text="Nombre de usuario:", bg="#4287f5", fg="#000000", font=("Helvetica", 16))
        label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.root, font=("Helvetica", 18))
        self.entry_username.pack()

        label_password = tk.Label(self.root, text="Contraseña:", bg="#4287f5", fg="#000000", font=("Helvetica", 16))
        label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.root, show="*", font=("Helvetica", 18))
        self.entry_password.pack()

        # Crear el botón de inicio de sesión
        button_login = tk.Button(self.root, text="Iniciar sesión", command=self.check_login, bg="#00cc00", fg="#000000", font=("Helvetica", 16))
        button_login.pack(pady=20)

    def check_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.instancia.escribirBitacora(f"Input - Inicio Sesion - Usuario: {username}")

        if self.checkData(username, password):
            self.instancia.escribirBitacora("Output - Inicio Sesion - Inicio de sesion Exitoso")
            messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
            self.root.destroy()
            mainWindow = MainWindow()
            
        else:
            self.instancia.escribirBitacora("Output - Inicio Sesion - Inicio de sesion Fallido")
            messagebox.showerror("Inicio de sesión", "Nombre de usuario o contraseña incorrectos")
            

    def decryptPassword(self,ciphertext, key):
        # Convierte la clave y el texto cifrado a bytes
        key = bytes.fromhex(key)
        ciphertext = bytes.fromhex(ciphertext)
        
        # Crea el objeto de cifrado
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()
        
        # Desencripta el texto cifrado
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remueve el padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        # Retorna el password desencriptado como una cadena de texto
        return plaintext.decode()

    def checkData(self,usuario, password):
        try:
            with open("Archivos/users.txt", "r") as archivo:
                lineas = archivo.readlines()
                for i in range(0, len(lineas), 2):  # Saltar de dos en dos para leer el usuario y la contraseña en cada iteración
                    usuario_archivo = lineas[i].strip()
                    password_archivo = lineas[i+1].strip()

                    if usuario == usuario_archivo:
                        ciphertext = str(password_archivo)  # El password cifrado del archivo users.txt
                        key = "miaproyecto12345"  # La clave de encriptación
                        # Convierte la clave en formato ASCII a hexadecimal
                        key_hex = binascii.hexlify(key.encode()).decode()
                        password_desencriptado = self.decryptPassword(ciphertext, key_hex)
                        if password == password_desencriptado:
                            return True
            return False
        
        except IOError:
            print("Error al leer el archivo.")
            self.instancia.escribirBitacora(f'Output - Login - Error al leer el archivo users.txt')
            return False

    def run(self):
        self.root.mainloop()
