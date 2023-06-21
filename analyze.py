import re
import os
from tkinter import messagebox
import os

from Commands.Create import Create
from Commands.Delete import Delete
from Commands.Copy import Copy
from Commands.Transfer import Transfer
from Commands.Rename import Rename
from Commands.Modify import Modify
from Commands.Add import Add
from Commands.Backup import Backup
from Singleton import Singleton

class Analyze():
    def __init__(self, commands):
        self.commands = commands
        self.lines = []
        self.parameters = []
        self.commandList = [
                            "configure", 
                            "create", 
                            "delete", 
                            "copy", 
                            "transfer", 
                            "rename", 
                            "modify", 
                            "add", 
                            "backup",
                            "exec"
                        ]
        self.configure = False # Sirve para verificar cada vez que se corre la consola si el configure viene o no
        self.exec = False # Sirve para verificar cada vez que se corre la consola si el exec viene o no
        self.instancia=Singleton.getInstance()
        self.ReadEncript=False
        
    def analyze(self):
        self.lines = self.commands.splitlines()
        # self.lines = re.split(r'\\n', self.commands)
        # print(self.lines)
        for i in range(len(self.lines)):
            if self.ReadEncript:
                nuevosComandos=self.instancia.decryptText(self.lines[i])
                self.instancia.ventana.agregarEntrada(nuevosComandos)
                self.instancia.ventana.AnalizadorNuevo(nuevosComandos)
                # print(nuevosComandos)
                continue
            if str(self.lines[i]).strip() == "":
                continue
            command = self.lines[i].split()
            if str(command[0]).lower() in self.commandList:
                if i == 0:
                    if str(command[0]).lower() == "configure":
                        self.configure = True
                        if not self.Configure(self.lines[i]):
                            return
                    elif str(command[0]).lower() == "exec":
                        self.exec = True
                        self.Exec(self.lines[i])
                    else:
                        self.instancia.consola += "Error, se debe usar el comando 'configure' o 'exec' de primero.\n"
                        print("Error, se debe usar el comando 'configure' o 'exec' de primero.")
                        return
                elif str(command[0]).lower() == "create":
                    self.Create(self.lines[i])
                elif str(command[0]).lower() == "delete":
                    self.Delete(self.lines[i])
                elif str(command[0]).lower() == "copy":
                    self.Copy(self.lines[i])
                elif str(command[0]).lower() == "transfer":
                    self.Transfer(self.lines[i])
                elif str(command[0]).lower() == "rename":
                    self.Rename(self.lines[i])
                elif str(command[0]).lower() == "modify":
                    self.Modify(self.lines[i])
                elif str(command[0]).lower() == "add":
                    self.Add(self.lines[i])
                elif str(command[0]).lower() == "backup":
                    self.Backup()
            else:
                print(f"Este comando no existe: {command[0]}")
                self.instancia.consola += f"Este comando no existe: {command[0]}\n"
                continue
   
    
 
    def Create(self, command):
        name = None
        body = None
        path = None
        
        current = command.split(" -")
        if len(current) < 4 or len(current) > 4:
            print("Error, la cantidad de parámetros es incorrecta.")
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: create.")
                self.instancia.consola += "Error con los parámetros de: create.\n"
                return
            
            if str(parametro[0]).lower() == "name":
                # Verificar si la cadena tiene espacios en blanco
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    # Verificar si hay comillas dobles al principio y al final
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        # Eliminar las comillas y realizar un strip
                        parametro[1] = parametro[1][1:-1].strip()
                    else:
                        print('Error, el nombre del archivo tiene espacios en blanco y no está dentro de "".')
                        self.instancia.consola += 'Error, el nombre del archivo tiene espacios en blanco y no está dentro de "".\n'
                        return  
                else:
                    # Verificar si hay comillas dobles al principio y al final
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        # Eliminar las comillas
                        parametro[1] = parametro[1][1:-1]
                name = parametro[1]
            elif str(parametro[0]).lower() == "body":
                parametro[1] = str(parametro[1]).strip()
                if parametro[1].startswith('"') and parametro[1].endswith('"'):
                    body = parametro[1][1:-1]
                else:
                    print('Error, el body del archivo no está dentro de "".')
                    self.instancia.consola += 'Error, el body del archivo no está dentro de "".\n'
                    return  
            elif str(parametro[0]).lower() == "path":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                        
                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return  
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                            
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                path = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if name is not None and body is not None and path is not None:
            create = Create(name, body, path)
            if self.instancia.type=="local":
                create.Local()
            elif self.instancia.type=="cloud":
                create.Cloud()
        else:
            print("Error con los parámetros obligatorios del comando: Create")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Create\n"
            return
 
    def Delete(self, command):
        name = None
        path = None
        
        current = command.split(" -")
        if len(current) < 2 or len(current) > 3:
            print("Error, la cantidad de parámetros es incorrecta.")
             
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: delete.")
                 
                self.instancia.consola += "Error con los parámetros de: delete.\n"
                return
            
            if str(parametro[0]).lower() == "name":
                # Verificar si la cadena tiene espacios en blanco
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    # Verificar si hay comillas dobles al principio y al final
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        # Eliminar las comillas y realizar un strip
                        parametro[1] = parametro[1][1:-1].strip()
                    else:
                        print('Error, el nombre del archivo tiene espacios en blanco y no está dentro de "".')
                         
                        self.instancia.consola += 'Error, el nombre del archivo tiene espacios en blanco y no está dentro de "".\n'
                        return  
                else:
                    # Verificar si hay comillas dobles al principio y al final
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        # Eliminar las comillas
                        parametro[1] = parametro[1][1:-1]
                name = parametro[1]
            elif str(parametro[0]).lower() == "path":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                        
                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                path = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if path is not None:
             
            respuesta = messagebox.askquestion("Eliminar archivo", f"¿Deseas eliminar el archivo {name}?")
            if respuesta == "yes":
                delete = Delete(path, name)
                if self.instancia.type=="local":
                    delete.Local()
                elif self.instancia.type=="cloud":
                    delete.Cloud()
        else:
            print("Error con los parámetros obligatorios del comando: Delete")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Delete\n"
            return
 
    def Copy(self, command):
        pfrom = None
        pto = None
        
        current = command.split(" -")
        if len(current) < 3 or len(current) > 3:
            print("Error, la cantidad de parámetros es incorrecta.")
             
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: copy.")
                 
                self.instancia.consola += "Error con los parámetros de: copy.\n"
                return
            
            if str(parametro[0]).lower() == "from":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                        
                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                pfrom = parametro[1]
            elif str(parametro[0]).lower() == "to":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                         
                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                pto = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if pfrom is not None and pto is not None:
            copy = Copy(pfrom, pto)
            if self.instancia.type=="local":
                copy.Local()
            elif self.instancia.type=="cloud":
                copy.Cloud()
        else:
            print("Error con los parámetros obligatorios del comando: Copy")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Copy\n"
            return
 
    def Transfer(self, command):
        pfrom = None
        pto = None
        mode = None
        
        current = command.split(" -")
        if len(current) < 4 or len(current) > 4:
            print("Error, la cantidad de parámetros es incorrecta.")
             
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: transfer.")
                 
                self.instancia.consola += "Error con los parámetros de: transfer.\n"
                return
            
            if str(parametro[0]).lower() == "from":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]

                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                pfrom = parametro[1]
            elif str(parametro[0]).lower() == "to":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]

                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                pto = parametro[1]
            elif str(parametro[0]).lower() == "mode":
                if parametro[1].startswith('"') and parametro[1].endswith('"'):
                    # Eliminar las comillas y realizar un strip
                    parametro[1] = parametro[1][1:-1].strip()
                if str(parametro[1]).lower() == "local" or str(parametro[1]).lower() == "cloud":
                    mode = str(parametro[1]).lower()
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += "Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if pfrom is not None and pto is not None and mode is not None:
            transfer = Transfer(pfrom, pto, mode)
            if self.instancia.type=="local":
                transfer.Local()
            elif self.instancia.type=="cloud":
                transfer.Cloud()
            
        else:
            print("Error con los parámetros obligatorios del comando: Transfer")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Transfer\n"
            return
      
    def Rename(self, command):
        name = None
        path = None
        
        current = command.split(" -")
        if len(current) < 3 or len(current) > 3:
            print("Error, la cantidad de parámetros es incorrecta.")
             
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: rename.")
                 
                self.instancia.consola += "Error con los parámetros de: rename.\n"
                return
            
            if str(parametro[0]).lower() == "name":
                # Verificar si la cadena tiene espacios en blanco
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    # Verificar si hay comillas dobles al principio y al final
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        # Eliminar las comillas y realizar un strip
                        parametro[1] = parametro[1][1:-1].strip()
                    else:
                        print('Error, el nombre del archivo tiene espacios en blanco y no está dentro de "".')
                         
                        self.instancia.consola += 'Error, el nombre del archivo tiene espacios en blanco y no está dentro de "".\n'
                        return  
                else:
                    # Verificar si hay comillas dobles al principio y al final
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        # Eliminar las comillas
                        parametro[1] = parametro[1][1:-1]
                name = parametro[1]
            elif str(parametro[0]).lower() == "path":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]

                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                path = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if path is not None and name is not None:
            rename = Rename(path, name)
            if self.instancia.type=="local":
                rename.Local()
            elif self.instancia.type=="cloud":
                rename.Cloud()
            
        else:
            print("Error con los parámetros obligatorios del comando: Rename")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Rename\n"
            return
         
    def Modify(self, command):
        body = None
        path = None
        
        current = command.split(" -")
        if len(current) < 3 or len(current) > 3:
            print("Error, la cantidad de parámetros es incorrecta.")
             
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: modify.")
                 
                self.instancia.consola += "Error con los parámetros de: modify.\n"
                return
            
            if str(parametro[0]).lower() == "body":
                parametro[1] = str(parametro[1]).strip()
                if parametro[1].startswith('"') and parametro[1].endswith('"'):
                    body = parametro[1][1:-1]
                else:
                    print('Error, el body del archivo no está dentro de "".')
                     
                    self.instancia.consola += 'Error, el body del archivo no está dentro de "".\n'
                    return  
            elif str(parametro[0]).lower() == "path":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]

                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                path = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if body is not None and path is not None:
            modify = Modify(path, body)
            if self.instancia.type=="local":
                modify.Local()
            elif self.instancia.type=="cloud":
                modify.Cloud()
            
        else:
            print("Error con los parámetros obligatorios del comando: Modify")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Modify\n"
            return
     
    def Add(self, command):
        body = None
        path = None
        
        current = command.split(" -")
        if len(current) < 3 or len(current) > 3:
            print("Error, la cantidad de parámetros es incorrecta.")
             
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: add.")
                 
                self.instancia.consola += "Error con los parámetros de: add.\n"
                return
            
            if str(parametro[0]).lower() == "body":
                parametro[1] = str(parametro[1]).strip()
                if parametro[1].startswith('"') and parametro[1].endswith('"'):
                    body = parametro[1][1:-1]
                else:
                    print('Error, el body del archivo no está dentro de "".')
                     
                    self.instancia.consola += 'Error, el body del archivo no está dentro de "".\n'
                    return  
            elif str(parametro[0]).lower() == "path":
                parametro[1] = str(parametro[1]).strip()
                if ' ' in parametro[1]:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]

                    newPath = ""
                    for cruta in str(parametro[1]).split("/"):
                        if " " in cruta:
                            if cruta.startswith('"') and cruta.endswith('"'):
                                # Eliminar las comillas y realizar un strip
                                newPath += cruta[1:-1].strip()
                                newPath += "/"
                            else:
                                print('Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".')
                                 
                                self.instancia.consola += 'Error, la ruta del archivo tiene espacios en blanco y no está dentro de "".\n'
                                return
                        else:
                            newPath += cruta.strip()
                            newPath += "/"
                    
                    parametro[1] = newPath[:-1]
                else:
                    if parametro[1].startswith('/'):
                        parametro[1] = parametro[1][1:]
                    if parametro[1].endswith('/'):
                        parametro[1] = parametro[1][:-1]
                    parametro[1] = parametro[1].strip()
                path = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if body is not None and path is not None:
            add = Add(path, body)
            if self.instancia.type=="local":
                add.Local()
            elif self.instancia.type=="cloud":
                add.Cloud()
            
        else:
            print("Error con los parámetros obligatorios del comando: Add")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Add\n"
            return
         
    def Backup(self):
        # Codigo para realizar el backup
        backup = Backup()
        instancia = Singleton.getInstance()
        if instancia.type == "local":
            backup.Local()
        elif instancia.type == "cloud":
            backup.Cloud()