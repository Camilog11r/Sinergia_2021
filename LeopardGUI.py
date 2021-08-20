import PyQt5
import tkinter as tk
from tkinter import ttk

#Creacion de clase tk
window = tk.Tk()
#Colocar el titulo del proyecto
window.title("Leopard Project")

#Redimencionamiento de la pantalla principal
window.resizable(False,False)

#Agregrar una etiqueta
a_label=ttk.Label(window,text="Principal Aplicacion de registros").grid(column=0,row=0) #Etiqueta de solo texto

#definicion de la funcion del botón
def well_log():
    action.configure(text='Hola amigo ' + name.get())


#Agregar el Botón
action = ttk.Button(window, text="Ingresa un nombre", command=well_log) #Etiqueta de boton
action.grid(column=2,row=1)
#action.configure(state='disabled') Desabilita el boton

#Creacion de una caja de texto enlazado con la función well_log
name = tk.StringVar() ##Importante, crea una variable de cadena para utilizarlo en una función
name_entered = ttk.Entry(window, width=12, textvariable=name) #Etiqueta de entrada de texto
name_entered.grid(column=0,row=1)

#Ubica el cursos del usuario en la entrada del widget
name_entered.focus()

#Creación de una nueva etiqueta
combobox = ttk.Combobox(window, width=12, textvariable=number)
combobox['value'] = ('Ecuacion de Indonesia','Ecuación de labeles')
combobox.grid(column=1, row=0)
combobox.current(0)


#Inicio de la aplicación
window.mainloop()