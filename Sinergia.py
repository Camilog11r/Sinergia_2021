from tkinter import *
import tkinter

ventana = tkinter.Tk()
ventana.geometry("960x460")

def cajita():
    numero = cajatexto.get()
    print(numero)

etiqueta = tkinter.Label(ventana, text = "Sinergia 2021")
etiqueta.pack() #Etiqueta en la parte de arriba

creacion = tkinter.Button(ventana, text ="Presiona",padx= 40,pady = 50,command=cajita)
creacion.pack(side=RIGHT)

cajatexto = tkinter.Entry(ventana,font="Helvetica 30")
cajatexto.pack()

ventana.mainloop()

