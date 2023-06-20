import os
from datetime import datetime
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
        self.ventana=None
        self.consola=""
        self.type=""
        self.encriptlog=False
        self.read=False
        self.llave=""
        self.consola = ""
        self.directorio_credenciales = 'credentials_module.json'
        self.id_folder = '1HrpmEeW8X3c3fSA7oaBsgymfDD7zVB3r'
        self.cLocal=0
        self.cNube=0
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

    def logout(self):
        self.type=""
        self.encriptlog=False
        self.read=False
        self.llave=""
        self.cLocal=0
        self.cNube=0

    def addConsola(self,texto):
        self.consola+=texto
    
    def getConsola(self)-> str:
        return self.consola
    
    def definir_configuracion(self, tipo:str, encriptadoLog:str, encriptadoRead:str,llave:str):
        if len(llave)>16 and (encriptadoLog=="true" or encriptadoRead=="true"):
            print("Error, la llave debe de ser de 16 caracteres")
            self.escribirBitacora(f'Output - Configure - Error, la llave debe de ser de 16 caracteres')
            self.consola += "Error, la llave debe de ser de 16 caracteres\n"
            # self.ventana.printTerminal()
            return False
        elif len(llave)<16 and (encriptadoLog=="true" or encriptadoRead=="true"):
            print("Error, la llave debe de ser de 16 caracteres")
            self.escribirBitacora(f'Output - Configure - Error, la llave debe de ser de 16 caracteres')
            self.consola += "Error, la llave debe de ser de 16 caracteres\n"
            # self.ventana.printTerminal()
            return False
        elif len(llave)==16 and (encriptadoLog=="true" or encriptadoRead=="true"):
            self.llave=llave
        else:
            self.llave=llave

        self.type=tipo
        if encriptadoLog=="true":
            self.encriptlog=True
        else:
            self.encriptlog=False

        if encriptadoRead=="true":
            self.encriptread=True
        else:
            self.encriptread=False
        return True

        
            


    def escribirBitacora(self, texto):
        data = datetime.now()
        dia = data.day
        mes = data.month
        año = data.year

        hora = data.hour
        minutos = data.minute
        segundos = data.second

        filename = f"./Archivos/{año}/{mes}/{dia}/log_archivos.txt"
        contenido = f"{dia}/{mes}/{año} {hora}:{minutos}:{segundos} - "+texto+"\n"
        if self.encriptlog:
            linea=self.encryptLinea(contenido, self.llave)
            contenido=linea+"\n"
        with open(filename, "a") as file:
            file.write(contenido)
        file.close()

    def encryptLinea(self, texto:str, llave:str):
        # Convierte la clave y el texto en bytes
        llave = llave.encode().hex()
        texto = texto.encode()

        # Añade el padding al texto plano
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(texto) + padder.finalize()

        # Crea el objeto de cifrado
        backend = default_backend()
        cipher = Cipher(algorithms.AES(bytes.fromhex(llave)), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()

        # Encripta el texto plano
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        # Convierte el texto cifrado a formato hexadecimal
        ciphertext_hex = binascii.hexlify(ciphertext).decode()
        # Retorna el texto cifrado en formato hexadecimal
        return ciphertext_hex
    

    def decryptText(self,ciphertext):
        # Convierte la clave y el texto cifrado a bytes
        key=self.llave
        key = binascii.hexlify(key.encode()).decode()
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
        
        # Retorna el text desencriptado como una cadena de texto
        desencriptado=plaintext.decode()
        comando=f"Configure -type->{self.type} -encrypt_log->{self.encriptlog} -encrypt_read->false -llave->{self.llave}\n"
        return comando+desencriptado
    
    def login(self):
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = self.directorio_credenciales
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(self.directorio_credenciales)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile(self.directorio_credenciales)
        credenciales = GoogleDrive(gauth)
        return credenciales    