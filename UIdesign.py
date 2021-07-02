from tkinter import *
from typing import Collection
x = 0
#Funciones
def API():
    x = textbox1.get()
    api = (141.5 / x ) - 131.5
    print (api)
    return


#Diseño de la página inicial
window = Tk()
window.title("Backend Oil Service")
window.config(bg='#fff')

#Creación de etiquetas
etiquetas = Label(window,text="Bienvenido a la Primera Version del Programa \n Backend Oil services",anchor=N).grid(row=1,column=1)
etiqueta1 = Label(window,text="Ingrese el valor de gravedad especifica").grid(row=2,column=0)
# etiqueta2 = Label(window,text="Ingrese el valor de").grid(row=3,column=0)
# etiqueta3 = Label(window,text="Ingrese el valor de").grid(row=4,column=0)
# etiqueta4 = Label(window,text="Ingrese el valor de").grid(row=5,column=0)

#Creación de botones
boton1 = Button(window,text="Primer boton",fg="#000",command=API,font='Helvetica 12').grid(row=2,column=1)
boton2 = Button(window,text="Segundo boton",fg="red",relief=FLAT).grid(row=3,column=1)
boton3 = Button(window,text="Tercer boton",fg="#479",relief=RIDGE).grid(row=4,column=1)
boton3 = Button(window,text="Cuerto boton",fg="red").grid(row=5,column=1)
boton4 = Button(window,bitmap='error').grid(row=5,column=5)


#Creación de cuadros de texto
textbox1 = Entry(window).grid(row=2,column=2)
textbox2 = Entry(window).grid(row=3,column=2)
textbox3 = Entry(window).grid(row=4,column=2)
textbox4 = Entry(window).grid(row=5,column=2)

#Imagenes
imagen1 = PhotoImage(file='./Images/ob.png')
fondo = Label(window,image=imagen1).grid(row=0,column=8)


window.mainloop()