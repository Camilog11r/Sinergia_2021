import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
# Subclass QMainWindow to customize your application's main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.button_is_checked = True
        
        #Customizacion de la aplicación
        self.setWindowTitle("Jaguar project")
        self.setFixedSize(300,300)
        
        #Opciones para los botones
        button = QPushButton("Let´s go")
        button.setCheckable(True)
        #button.clicked.connect(self.the_button_was_clicked) #Realiza una accion de respuesta al clickeo
        button.clicked.connect(self.the_button_was_toggled) #Realiza una accion de alternancia

        
        # Set the central widget of the Window.
        self.setCentralWidget(button)
        
    # #Creacion de señal al cliqueo
    # def the_button_was_clicked(self):
    #     print("clicked")
    
    #Da resultado de True o False respecto a una acción
    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print(self.button_is_checked)

app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
