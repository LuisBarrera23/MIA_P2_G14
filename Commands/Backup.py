import os
from Singleton import Singleton

class Backup():
    def __init__(self,typeto, typefrom, ip, port, name) -> None:
        self.typeto=typeto
        self.typefrom=typefrom
        self.ip=ip
        self.port=port
        self.name=name
        self.instancia = Singleton.getInstance()
        
    def run(self):
        pass
    
    def Local(self):
        pass
    
    def Cloud(self):
        pass