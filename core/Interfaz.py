import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QComboBox, QTextEdit, QProgressBar, QSlider
from interfaz_ui import Ui_MainWindow


class Interfaz(QMainWindow):
    lista_programas = []
    senial = Signal(list)
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Se conecta cada combobox con la funcion _combo_changed(c)

        self.combos = [
            self.ui.comboBoxPot1,
            self.ui.comboBoxPot2,
            self.ui.comboBoxPot3,
            self.ui.comboBoxPot4,
            self.ui.comboBoxPot5
        ]
        for combo in self.combos:
            combo.currentIndexChanged.connect(lambda _, c=combo: self._combo_changed(c))


        ## Diccionario que guarda a que hace referencia cada nombre en las seniales
        self._mapa_elementos = {
            "COMBOBOX_ARDUINO": self.ui.comboBox_2,
            "COMBOBOX_DISP": self.ui.comboBox,
            "COMBOBOX_POT2": self.ui.comboBoxPot1,
            "COMBOBOX_POT3": self.ui.comboBoxPot2,
            "COMBOBOX_POT4": self.ui.comboBoxPot3,
            "COMBOBOX_POT5": self.ui.comboBoxPot4,
            "COMBOBOX_POT6": self.ui.comboBoxPot5,
            "LOG": self.ui.textEdit,
            "NIVEL_D": self.ui.progressBar,
            "NIVEL_I": self.ui.progressBar_2,
            "SLIDER_POT1": self.ui.Slider1,
            "SLIDER_POT2": self.ui.Slider2,
            "SLIDER_POT3": self.ui.Slider3,
            "SLIDER_POT4": self.ui.Slider4,
            "SLIDER_POT5": self.ui.Slider5,
            "SLIDER_MASTER": self.ui.masterSlider,
            "LISTA_PROGRAMAS": self.lista_programas
        }
    def inicializar(self):
        #Aca se inicializan las seniales de los objetos que pueden llegar a generarlas
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_4.clicked.connect(lambda: self.senial.emit(["BOTON","conectar_arduino",self.ui.comboBox_2.currentText()]))
        self.ui.pushButton_3.clicked.connect(lambda: self.senial.emit(["BOTON","encender_luz"]))
        self.ui.pushButton_2.clicked.connect(lambda: self.senial.emit(["BOTON","iniciar"]))
        self.ui.comboBox.currentIndexChanged.connect(lambda: self.senial.emit(["COMBOBOX_DISP", self.ui.comboBox.currentText()]))
        self.ui.comboBox_2.currentIndexChanged.connect(lambda: self.senial.emit(["COMBOBOX_ARDUINO",self.ui.comboBox_2.currentText()]))

    def _combo_changed(self, combo):
        #Hubo un cambio en un combobox
        seleccionado = combo.currentText()

        if not seleccionado:
            return

        for otro in self.combos:
            if otro is not combo and otro.currentText() == seleccionado:
                otro.blockSignals(True)
                otro.setCurrentIndex(-1)
                otro.blockSignals(False)
                self.senial.emit([otro.objectName(), None])

        self.senial.emit([combo.objectName(),seleccionado])

    def actualizar(self,senial):
        elemento = self._mapa_elementos.get(senial[0])


        if elemento is not None:
            if isinstance(elemento, list):

                self.lista_programas = senial[1]
                for combo in self.combos:
                    actual = combo.currentText()
                    combo.blockSignals(True)
                    combo.clear()
                    combo.addItems(self.lista_programas)

                    if actual in self.lista_programas:
                        combo.setCurrentText(actual)
                    else:
                        combo.setCurrentIndex(-1)
                    combo.blockSignals(False)

            if isinstance(elemento,QComboBox):
                for puerto in senial[1]:
                    nombre = puerto.name
                    elemento.addItem(nombre)
                    print(nombre)


                elemento.setCurrentIndex(0)
            if isinstance(elemento, QTextEdit):
                elemento.append(senial[1])
            if isinstance(elemento, QProgressBar) or isinstance(elemento, QSlider):
                elemento.setValue(int(senial[1]))

        else:
            pass
            ##mandar una advertencia que no se encontro ese elemento

    def mostrar(self):
        self.show()