import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from interfaz_ui import Ui_MainWindow


class Interfaz(QMainWindow):
    seniales = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def inicializar(self):
        #Aca se inicializa lo que hay que cambiar de la interfaz a la hora de crearla
        self.ui.textEdit.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_4.clicked.connect(lambda: self.seniales.emit("ja"))
        self.ui.pushButton_3.clicked.connect(lambda: self.seniales.emit("cambiar_luz"))
        self.ui.pushButton_2.clicked.connect(lambda: self.seniales.emit("iniciar"))

    def mostrar(self):
        self.show()