import os

from Commands.Create import Create
from Commands.Delete import Delete
from Commands.Copy import Copy
from Commands.Transfer import Transfer
from Commands.Rename import Rename
from Commands.Modify import Modify
from Commands.Backup import Backup
from Commands.Recovery import Recovery
from Commands.DeleteAll import DeleteAll
from Commands.Open import Open
from Singleton import Singleton

class Analyze():
    def __init__(self, commands):
        self.commands = commands
        self.lines = []
        self.parameters = []
        self.commandList = [
                            "create", 
                            "delete", 
                            "copy", 
                            "transfer", 
                            "rename", 
                            "modify", 
                            "backup",
                            "recovery",
                            "delete_all",
                            "open"
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
                if str(command[0]).lower() == "create":
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
                elif str(command[0]).lower() == "backup":
                    self.Backup(self.lines[i])
                elif str(command[0]).lower() == "recovery":
                    self.Recovery(self.lines[i])
                elif str(command[0]).lower() == "delete_all":
                    self.DeleteAll(self.lines[i])
                elif str(command[0]).lower() == "open":
                    self.Open(self.lines[i])
            else:
                print(f"Este comando no existe: {command[0]}")
                self.instancia.consola += f"Este comando no existe: {command[0]}\n"
                continue

    def Create(self, command):
        name = None
        body = None
        path = None
        type = None
        
        current = command.split(" -")
        if len(current) < 5 or len(current) > 5:
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
            elif str(parametro[0]).lower() == "type":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type = parametro[1]
                else:
                    print(f'Error, este valor de type no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type no existe:{parametro[1]}.\n'
                    return  
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if name is not None and body is not None and path is not None and type is not None:
            create = Create(name, body, path,type)
            create.run()
        else:
            print("Error con los parámetros obligatorios del comando: Create")
             
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Create\n"
            return
 
    def Delete(self, command):
        name = None
        path = None
        type = None
        
        current = command.split(" -")
        if len(current) < 3 or len(current) > 4:
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
            elif str(parametro[0]).lower() == "type":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type = parametro[1]
                else:
                    print(f'Error, este valor de type no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type no existe:{parametro[1]}.\n'
                    return  
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if path is not None and type is not None:
            # respuesta = messagebox.askquestion("Eliminar archivo", f"¿Deseas eliminar el archivo {name}?") Preguntar si se elimina o no
            if True:
                delete = Delete(path, name, type)
                delete.run()
        else:
            print("Error con los parámetros obligatorios del comando: Delete")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Delete\n"
            return
 
    def Copy(self, command):
        pfrom = None
        pto = None
        type_to = None
        type_from = None
        
        current = command.split(" -")
        if len(current) < 5 or len(current) > 5:
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
            elif str(parametro[0]).lower() == "type_to":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_to = parametro[1]
                else:
                    print(f'Error, este valor de type_to no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_to no existe:{parametro[1]}.\n'
                    return
            elif str(parametro[0]).lower() == "type_from":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_from = parametro[1]
                else:
                    print(f'Error, este valor de type_from no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_from no existe:{parametro[1]}.\n'
                    return
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if pfrom is not None and pto is not None and type_to is not None and type_from is not None:
            copy = Copy(pfrom, pto, type_to, type_from)
            copy.run()
        else:
            print("Error con los parámetros obligatorios del comando: Copy")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Copy\n"
            return
 
    def Transfer(self, command):
        pfrom = None
        pto = None
        type_to = None
        type_from = None
        
        current = command.split(" -")
        if len(current) < 5 or len(current) > 5:
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
            elif str(parametro[0]).lower() == "type_to":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_to = parametro[1]
                else:
                    print(f'Error, este valor de type_to no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_to no existe:{parametro[1]}.\n'
                    return
            elif str(parametro[0]).lower() == "type_from":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_from = parametro[1]
                else:
                    print(f'Error, este valor de type_from no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_from no existe:{parametro[1]}.\n'
                    return  
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += "Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if pfrom is not None and pto is not None and type_to is not None and type_from is not None:
            transfer = Transfer(pfrom, pto, type_to, type_from)
            transfer.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Transfer")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Transfer\n"
            return
      
    def Rename(self, command):
        name = None
        path = None
        type = None
        
        current = command.split(" -")
        if len(current) < 4 or len(current) > 4:
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
            elif str(parametro[0]).lower() == "type":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type = parametro[1]
                else:
                    print(f'Error, este valor de type no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type no existe:{parametro[1]}.\n'
                    return  
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                 
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if path is not None and name is not None and type is not None:
            rename = Rename(path, name, type)
            rename.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Rename")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Rename\n"
            return
         
    def Modify(self, command):
        body = None
        path = None
        type = None
        
        current = command.split(" -")
        if len(current) < 4 or len(current) > 4:
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
            elif str(parametro[0]).lower() == "type":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type = parametro[1]
                else:
                    print(f'Error, este valor de type no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type no existe:{parametro[1]}.\n'
                    return  
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if body is not None and path is not None and type is not None:
            modify = Modify(path, body, type)
            modify.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Modify")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Modify\n"
            return

    def Backup(self, command):
        type_to = None
        type_from = None
        ip = None
        port = None
        name = None
        
        current = command.split(" -")
        if len(current) < 4 or len(current) > 6:
            print("Error, la cantidad de parámetros es incorrecta.")
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: Backup.")
                self.instancia.consola += "Error con los parámetros de: Backup.\n"
                return
            
            if str(parametro[0]).lower() == "type_to":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_to = parametro[1]
                else:
                    print(f'Error, este valor de type_to no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_to no existe:{parametro[1]}.\n'
                    return  
            elif str(parametro[0]).lower() == "type_from":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_from = parametro[1]
                else:
                    print(f'Error, este valor de type_from no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_from no existe:{parametro[1]}.\n'
                    return  
            elif str(parametro[0]).lower() == "ip":
                parametro[1] = str(parametro[1]).strip()
                ip = parametro[1]
            elif str(parametro[0]).lower() == "port":
                parametro[1] = str(parametro[1]).strip()
                port = parametro[1]
            elif str(parametro[0]).lower() == "name":
                parametro[1] = str(parametro[1]).strip()
                if " " in parametro[1]:
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        parametro[1] = parametro[1][1:-1]
                    else:
                        print('Error, el name del archivo no está dentro de "".')
                        self.instancia.consola += 'Error, el name del archivo no está dentro de "".\n'
                        return
                elif parametro[1].startswith('"') and parametro[1].endswith('"'):
                    parametro[1] = parametro[1][1:-1]
                
                name = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if type_to is not None and type_from is not None and name is not None:
            backup = Backup(type_to, type_from, ip, port, name)
            backup.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Backup")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Backup\n"
            return

    def Recovery(self, command):
        type_to = None
        type_from = None
        ip = None
        port = None
        name = None
        
        current = command.split(" -")
        if len(current) < 4 or len(current) > 6:
            print("Error, la cantidad de parámetros es incorrecta.")
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: Recovery.")
                self.instancia.consola += "Error con los parámetros de: Recovery.\n"
                return
            
            if str(parametro[0]).lower() == "type_to":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_to = parametro[1]
                else:
                    print(f'Error, este valor de type_to no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_to no existe:{parametro[1]}.\n'
                    return  
            elif str(parametro[0]).lower() == "type_from":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type_from = parametro[1]
                else:
                    print(f'Error, este valor de type_from no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type_from no existe:{parametro[1]}.\n'
                    return  
            elif str(parametro[0]).lower() == "ip":
                parametro[1] = str(parametro[1]).strip()
                ip = parametro[1]
            elif str(parametro[0]).lower() == "port":
                parametro[1] = str(parametro[1]).strip()
                port = parametro[1]
            elif str(parametro[0]).lower() == "name":
                parametro[1] = str(parametro[1]).strip()
                if " " in parametro[1]:
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        parametro[1] = parametro[1][1:-1]
                    else:
                        print('Error, el name del archivo no está dentro de "".')
                        self.instancia.consola += 'Error, el name del archivo no está dentro de "".\n'
                        return
                elif parametro[1].startswith('"') and parametro[1].endswith('"'):
                    parametro[1] = parametro[1][1:-1]
                
                name = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if type_to is not None and type_from is not None and name is not None:
            recovery = Recovery(type_to, type_from, ip, port, name)
            recovery.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Recovery")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Recovery\n"
            return

    def DeleteAll(self, command):
        type = None
        
        current = command.split(" -")
        if len(current) < 2 or len(current) > 2:
            print("Error, la cantidad de parámetros es incorrecta.")
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: Delete_all.")
                self.instancia.consola += "Error con los parámetros de: Delete_all.\n"
                return
            
            if str(parametro[0]).lower() == "type":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type = parametro[1]
                else:
                    print(f'Error, este valor de type no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type no existe:{parametro[1]}.\n'
                    return  
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if type is not None:
            deleteAll = DeleteAll(type)
            deleteAll.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Delete_all")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Delete_all\n"
            return

    def Open(self, command):
        type = None
        ip = None
        port = None
        name = None
        
        current = command.split(" -")
        if len(current) < 3 or len(current) > 5:
            print("Error, la cantidad de parámetros es incorrecta.")
            self.instancia.consola += "Error, la cantidad de parámetros es incorrecta.\n"
            return
        
        for i in range(1,len(current)):
            parametro = current[i].split("->")
            if len(parametro) != 2:
                print("Error con los parámetros de: Open.")
                self.instancia.consola += "Error con los parámetros de: Open.\n"
                return
            
            if str(parametro[0]).lower() == "type":
                parametro[1] = str(parametro[1]).strip().lower()
                if parametro[1] == "server" or parametro[1] == "bucket":
                    type = parametro[1]
                else:
                    print(f'Error, este valor de type no existe:{parametro[1]}.')
                    self.instancia.consola += f'Error, este valor de type no existe:{parametro[1]}.\n'
                    return  
            elif str(parametro[0]).lower() == "ip":
                parametro[1] = str(parametro[1]).strip()
                ip = parametro[1]
            elif str(parametro[0]).lower() == "port":
                parametro[1] = str(parametro[1]).strip()
                port = parametro[1]
            elif str(parametro[0]).lower() == "name":
                parametro[1] = str(parametro[1]).strip()
                if " " in parametro[1]:
                    if parametro[1].startswith('"') and parametro[1].endswith('"'):
                        parametro[1] = parametro[1][1:-1]
                    else:
                        print('Error, el name del archivo no está dentro de "".')
                        self.instancia.consola += 'Error, el name del archivo no está dentro de "".\n'
                        return
                elif parametro[1].startswith('"') and parametro[1].endswith('"'):
                    parametro[1] = parametro[1][1:-1]
                
                name = parametro[1]
            else:
                print(f"Error, este parámetro no existe: {parametro[0]}.")
                self.instancia.consola += f"Error, este parámetro no existe: {parametro[0]}.\n"
                return
        
        if type is not None and name is not None:
            abrir = Open(type, ip, port, name)
            abrir.run()
            
        else:
            print("Error con los parámetros obligatorios del comando: Open")
            self.instancia.consola += "Error con los parámetros obligatorios del comando: Open\n"
            return