from tkinter import *
import tkinter

ventana = tkinter.Tk()
ventana.geometry("1080x960")

def cajita():
    numero = cajatexto.get()
    print(numero)

#Creacion de un texto
etiqueta = tkinter.Label(ventana, text = "Sinergia 2021")
etiqueta.pack() #Etiqueta en la parte de arriba

#Creacion de una caja de texto
cajatexto = tkinter.Entry(ventana,font="Helvetica 30")
cajatexto.pack()

#Creacion de un boton que realice una accion
creacion = tkinter.Button(ventana, text ="Presiona",width= 5, height=5,command=cajita)
creacion.pack()




ventana.mainloop()

