import os
from Singleton import Singleton

class Backup():
    def __init__(self) -> None:
        self.instancia = Singleton.getInstance()
        self.credenciales = self.instancia.login()
        self.idFolder = self.instancia.id_folder
        
    def Local(self):
        pass
    
    def Cloud(self):
        pass