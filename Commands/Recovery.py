import os
from Singleton import Singleton

class Recovery():
    def __init__(self,typeto, typefrom, ip, port, name) -> None:
        self.typeto=typeto
        self.typefrom=typefrom
        self.ip=ip
        self.port=port
        self.name=name
        self.consulta=False
        self.instancia = Singleton.getInstance()
        
    def run(self):
        if self.consulta:
            if self.typefrom == "server":
                return self.fromServer()
            elif self.typefrom == "bucket":
                return self.fromBucket()
        elif self.ip != None and self.port != None:
            if self.typeto == "server":
                self.toServer()
            elif self.typeto == "bucket":
                self.toBucket()
        elif self.typefrom == "server" and self.typeto == "bucket":
            self.Local()
        elif self.typefrom == "bucket" and self.typeto == "server":
            self.Cloud()
    
    def Local(self):
        pass
    
    def Cloud(self):
        pass

    def fromServer(self):
        pass

    def fromBucket(self):
        pass

    def toServer(self):
        pass
    
    def toBucket(self):
        pass