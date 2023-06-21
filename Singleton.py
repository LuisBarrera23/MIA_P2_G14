
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError

import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
class Singleton:

    __instance = None

   
    @staticmethod 
    def getInstance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance
    def __init__(self):
        self.consola = ""
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self


    def addConsola(self,texto):
        self.consola+=texto
    
    def getConsola(self)-> str:
        return self.consola

    

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
             
            return False   
        

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