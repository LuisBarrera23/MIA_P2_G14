import os
from Singleton import Singleton

class Open():
    def __init__(self,type, ip, port, name) -> None:
        self.type=type
        self.ip=ip
        self.port=port
        self.name=name
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.type=="server":
            self.Local()
        elif self.type=="bucket":
            self.Cloud()
    
    def Local(self):
        pass
    
    def Cloud(self):
        pass