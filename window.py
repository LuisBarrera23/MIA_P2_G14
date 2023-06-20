import tkinter
from tkinter import filedialog, Tk
from tkinter.constants import DISABLED
from tkinter.font import BOLD
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys
from os import system, startfile
import os
from PIL import Image, ImageTk
from tkinter import PhotoImage
from datetime import datetime

from Singleton import Singleton
from analyze import Analyze

# Funciones
# def Exit():
#     window.destroy()
#     sys.exit(0)

############################### Creation of the main window ###########################################
class MainWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Proyecto 1 - G14")
        self.window.iconbitmap("tedit.ico")
        self.window.update_idletasks()
        width = 1000
        height = 900
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, 140, 40))
        self.window.resizable(0, 0)
        self.instancia=Singleton.getInstance()

        # Set title
        label = tkinter.Label(self.window,
                            text="MIA Code Editor",
                            bg="#2980B9",
                            height=2,
                            fg='white',
                            font=('JetBrains Mono', 30, BOLD),
                            padx=0,
                            pady=0
                            )
        label.pack(fill='x')

        btn1 = tkinter.Button(self.window, command=self.configure, text="Configure", relief='groove', font=(
            'JetBrains Mono', 14), bg='#078aef', fg='white')
        btn1.place(x=0, y=110, width=120, height=30)
        
        self.btn2 = tkinter.Button(self.window, state='disabled', command=self.create,  text="Create", relief='groove', font=(
            'JetBrains Mono', 14), bg='#F99E0A', fg='black')
        self.btn2.place(x=120, y=110, width=90, height=30)

        self.btn3 = tkinter.Button(self.window, state='disabled',command=self.delete, text="Delete", relief='groove', font=(
            'JetBrains Mono', 14), bg='#F9F90A', fg='black')
        self.btn3.place(x=210, y=110, width=90, height=30)

        self.btn4 = tkinter.Button(self.window, state='disabled', command=self.copy, text="Copy", relief='groove', font=(
            'JetBrains Mono', 14), bg='#6CF90A', fg='black')
        self.btn4.place(x=300, y=110, width=70, height=30)
        
        self.btn5 = tkinter.Button(self.window, state='disabled',command=self.transfer, text="Transfer", relief='groove', font=(
            'JetBrains Mono', 14), bg='#00FFD8', fg='black')
        self.btn5.place(x=370, y=110, width=110, height=30)
        
        self.btn6 = tkinter.Button(self.window, state='disabled', command=self.rename, text="Rename", relief='groove', font=(
            'JetBrains Mono', 14), bg='#9E0AF9', fg='white')
        self.btn6.place(x=480, y=110, width=90, height=30)
        
        self.btn7 = tkinter.Button(self.window, state='disabled', command=self.modify, text="Modify", relief='groove', font=(
            'JetBrains Mono', 14), bg='#0AF9B4', fg='black')
        self.btn7.place(x=570, y=110, width=90, height=30)
        
        self.btn8 = tkinter.Button(self.window, state='disabled', command=self.add, text="Add", relief='groove', font=(
            'JetBrains Mono', 14), bg='#FFDC00', fg='black')
        self.btn8.place(x=660, y=110, width=60, height=30)

        self.btn9 = tkinter.Button(self.window, state='disabled', command=self.backup, text="Backup", relief='groove', font=(
            'JetBrains Mono', 14), bg='#009900', fg='white')
        self.btn9.place(x=720, y=110, width=90, height=30)

        btn10 = tkinter.Button(self.window, command=self.exec, text="Exec", relief='groove', font=(
            'JetBrains Mono', 14), bg='darkblue', fg='white')
        btn10.place(x=810, y=110, width=70, height=30)

        btn11 = tkinter.Button(self.window, command=self.log_out, text="Log Out", relief='groove', font=(
            'JetBrains Mono', 14), bg='red', fg='white')
        btn11.place(x=880, y=110, width=90, height=30)
        
        img = Image.open('run.png')
        img = img.resize((30, 30), Image.ANTIALIAS)  # Redimension (Alto, Ancho)
        img = ImageTk.PhotoImage(img)
        btn12 = tkinter.Button(self.window, text="Run", relief='groove', font=(
            'JetBrains Mono', 14), image=img, bd=0, command=self.Analizador)
        orig_color = btn12.cget("background")
        btn12.bind("<Enter>", func=lambda e: btn12.config(background="lightgray"))
        btn12.bind("<Leave>", func=lambda e: btn12.config(background=orig_color))
        btn12.place(x=970, y=110, width=30, height=30)

        
        self.instancia.ventana=self

        class LineNumbers(tkinter.Text):
            def __init__(self, master, text_widget, **kwargs):
                super().__init__(master, **kwargs)

                self.text_widget = text_widget
                self.text_widget.bind('<Return>', self.enter)

                self.insert(1.0, '1')
                self.configure(state='disabled')

            def enter(self, event=None):
                final_index = str(self.text_widget.index(tkinter.END))
                num_of_lines = final_index.split('.')[0]
                line_numbers_string = "\n".join(
                    str(no + 1) for no in range(int(num_of_lines)))
                width = len(str(num_of_lines))

                self.configure(state='normal', width=width)
                self.delete(1.0, tkinter.END)
                self.insert(1.0, line_numbers_string)
                self.configure(state='disabled')
                self.tag_configure("tag_name", justify='center')
                self.tag_add("tag_name", "1.0", "end")
                self.see("end")

        class ScrolledTextPair(Frame):
            '''Two Text widgets and a Scrollbar in a Frame'''

            def __init__(self, master, left, right, **kwargs):
                Frame.__init__(self, master)  # no need for super

        # Different default width
                if 'width' not in kwargs:
                    kwargs['width'] = 30

                # Creating the widgets
                self.left = left
                self.right = right
                self.scrollbar = Scrollbar(self)

                # Changing the settings to make the scrolling work
                self.scrollbar['command'] = self.on_scrollbar
                self.left['yscrollcommand'] = self.on_textscroll
                self.right['yscrollcommand'] = self.on_textscroll
                self.scrollbar.pack(side=RIGHT, fill=Y)

            def on_scrollbar(self, *args):
                '''Scrolls both text widgets when the scrollbar is moved'''
                self.left.yview(*args)
                self.right.yview(*args)

            def on_textscroll(self, *args):
                '''Moves the scrollbar and scrolls text widgets when the mousewheel
                is moved on a text widget'''
                self.scrollbar.set(*args)
                self.on_scrollbar('moveto', args[0])

        lbl2 = tkinter.Label(self.window, relief="sunken", border=20, bg='#2980B9')
        lbl2.place(x=0, y=140, width=1000, height=500)
        self.txt2 = tkinter.Text(lbl2, fg='navy', font=(
            'JetBrains Mono', 12), cursor='xterm red', insertbackground='red')
        self.lnumber = LineNumbers(lbl2, self.txt2, font=('JetBrains Mono', 12))
        self.lnumber.tag_configure("tag_name", justify='center')
        self.lnumber.tag_add("tag_name", "1.0", "end")
        self.lnumber.place(x=0, y=0, width=45, height=460)
        self.txt2.place(x=47, y=0, width=913, height=460)
        t = ScrolledTextPair(lbl2, self.lnumber, self.txt2, bg='white', fg='black')
        t.pack(side="right", fill='y')
        hs = ttk.Scrollbar(lbl2, orient=HORIZONTAL, command=self.txt2.xview)
        hs.pack(side="bottom", fill='x')
        self.txt2.configure(xscrollcommand=hs.set, wrap="none")
        lbl3 = tkinter.Label(self.window, relief="ridge", border=10)
        lbl3.place(x=0, y=640, width=1000, height=260)
        self.lbl4 = tkinter.Text(lbl3, relief="flat", bg='black',
                            fg="cyan", font=('JetBrains Mono', 12))
        self.lbl4.place(x=0, y=0, width=980, height=240)
        verscrlbar = ttk.Scrollbar(self.lbl4, orient=VERTICAL)
        horscrlbar = ttk.Scrollbar(self.lbl4, orient=HORIZONTAL)
        self.lbl4.insert(END, "@Proyecto 1 - G14\n")
        self.lbl4.tag_add("nombre", "1.0", "1.23")
        self.lbl4.tag_config("nombre",  foreground="yellow")
        self.lbl4["state"] = DISABLED
        self.window.mainloop()

    def configure(self):
        pass

    def create(self):
        pass
    
    def delete(self):
        pass

    def copy(self):
        pass

    def transfer(self):
        pass
    def rename(self):
        pass

    def modify(self):
        pass

    def add(self):
        pass

    def exec(self):
        pass

    def backup(self):
        from Commands.Backup import Backup
        back=Backup()
        if self.instancia.type=="local":
            back.Local()
        elif self.instancia.type=="cloud":
            back.Cloud()


    def agregarEntrada(self,texto:str):
        self.txt2.delete('1.0', 'end')
        lines=texto.split("\n")
        for i in lines:
            self.txt2.insert(END, i+"\n")
            self.lnumber.enter()
            
    def Analizador(self):
        text = self.txt2.get("1.0", tkinter.END)
        analizador = Analyze(text)
        analizador.analyze()
        self.instancia.ventana.printTerminal()

    def AnalizadorNuevo(self,text):
        analizador = Analyze(text)
        analizador.analyze()
        # self.instancia.ventana.printTerminal()

    def log_out(self):
        from login import Login
        self.instancia.logout()
        self.window.destroy()
        login =Login()
        login.run()
        pass


    def habilitarBotones(self):
        self.btn2.config(state='normal')
        self.btn3.config(state='normal')
        self.btn4.config(state='normal')
        self.btn5.config(state='normal')
        self.btn6.config(state='normal')
        self.btn7.config(state='normal')
        self.btn8.config(state='normal')
        self.btn9.config(state='normal')
        
    def printTerminal(self):
        self.lbl4["state"] = NORMAL
        self.lbl4.delete("1.0", END)
        self.lbl4.insert(END, "@Proyecto 1 - G14\n")
        self.lbl4.tag_add("nombre", "1.0", "1.23")
        self.lbl4.tag_config("nombre",  foreground="yellow")
        self.lbl4.insert(END, f"{self.instancia.consola}")
        self.lbl4["state"] = DISABLED
        self.instancia.consola = ""