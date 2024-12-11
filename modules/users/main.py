import socket
import sys
from tkinter import *
from PIL import ImageTk, Image
import os
from sys import byteorder
from tkinter import filedialog as fd

root = Tk()

root.title("Gogle")
root.resizable(False, False)
frame = Frame(root)




timeout = 3


minBuf = 1

RootPath = os.path.dirname(__file__)
RootPath += "/C_Archivos/"


def generate_intro():
    frame = Frame(root)
    LabelIntro = Label(frame,text="Bienvenido, las operaciones disponibles son:")
    Button_Register = Button(frame,text="Registrarse",command=lambda:generate_Register(frame))



    frame.pack()

def generate_Register(fram):
    global txtUsername
    global txtPassword
    
    frameR = Frame(root)
    fram.destroy()

    txtLabelUsername = Label(frameR,text="Ingresa un nombre de usuario:")
    txtUsername = Text(frameR,width=15,height=1)
    txtLabelPassword = Label(frameR,text="Ingresa una contraseña:")
    txtPassword = Text(frameR,width=15,height=1)
    RegisterButton = Button(frameR,text="Register",command=lambda:register(frameR))
    
    txtLabelUsername.grid(row=0,column=0)
    txtUsername.grid(row=1,column=0)
    txtLabelPassword.grid(row=2,column=0)
    txtPassword.grid(row=3,column=0)
    RegisterButton.grid(row=4,column=0)

    frameR.pack()

def register(fram):
    fram.destroy()
    Username = txtUsername.get(1.0,END)
    Password = txtPassword.get(1.0,END)
    
    
"""

def Operations():
	OperationFrame = Frame(root)
	label_comand = Label(OperationFrame,text="Las operaciones disponibles son:")
	button_Upload = Button(OperationFrame,text="Subir archivo",command=lambda:select_file())
	button_Download = Button(OperationFrame,text="Descargar archivo",command=lambda: Download_Frame(OperationFrame))
	button_CreateDirectory = Button(OperationFrame,text="Crear carpeta",command=lambda:Directory_Frame(OperationFrame))
	button_Delete = Button(OperationFrame, text="Eliminar archivo/directorio",command=lambda:Delete_Frame(OperationFrame))
	button_Rename = Button(OperationFrame,text="Cambiar nombre",command=lambda:Rename_Frame(OperationFrame))
	label_comand.grid(row=0,column=0)
	button_Upload.grid(row=1,column=0)
	button_Download.grid(row=2,column=0)
	button_CreateDirectory.grid(row=3,column=0)
	button_Delete.grid(row=4,column=0)
	button_Rename.grid(row=5,column=0)
	OperationFrame.pack()

"""

def main():
	generate_intro()
	mainloop()


if __name__ == '__main__':
	main()