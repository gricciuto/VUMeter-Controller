import sys
from queue import Queue

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QComboBox, QTextEdit, QProgressBar, QSlider

from core.Paquete import PaqueteSonido
from interfaz_ui import Ui_MainWindow


class Interfaz(QMainWindow):
    lista_programas = []
    senial = Signal(list)
    def __init__(self, bus: Queue):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bus = bus

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
            "COMBOBOX_ARDUINO": self.ui.comboBoxPuertosCOM,
            "COMBOBOX_DISP": self.ui.comboBoxMicrofonos,
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
        self.ui.botonSalir.clicked.connect(lambda: self.close())
        self.ui.comboBoxMicrofonos.currentIndexChanged.connect(lambda: self.senial.emit(["COMBOBOX_DISP", self.ui.comboBoxMicrofonos.currentText()]))
        self.ui.comboBoxPuertosCOM.currentIndexChanged.connect(lambda: self.senial.emit(["COMBOBOX_ARDUINO",self.ui.comboBoxPuertosCOM.currentText()]))
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
    def actualizarLista(self, elementos, combobox : str ):
        combo = self._mapa_elementos.get(combobox)
        for elemento in elementos:
            nombre = elemento.name
            combo.addItem(nombre)
        combo.setCurrentIndex(0)
    def getMicronofoSeleccionado(self):
        return self.ui.comboBoxMicrofonos.currentText()
    def getPuertoSeleccionado(self):
        return self.ui.comboBoxPuertosCOM.currentText()
    def arduinoConectado(self):
        self.ui.botonIniciar.setEnabled(True)
        self.ui.botonLuz.setEnabled(True)
        self.ui.textEdit.append("Arduino conectado")
    def setNiveles(self, paquete: PaqueteSonido):
        nivel_izquierdo, nivel_derecho = paquete.getPaqueteInterfaz()
        self.ui.progressBar.setValue(nivel_izquierdo)
        self.ui.progressBar_2.setValue(nivel_derecho)
    def mostrarError(self,error):
        self.ui.textEdit.append('<span style="color:red;">'+error+'</span>')
    def mostrarInfo(self,detalle):
        self.ui.textEdit.append(detalle)
    def actualizarPotenciometro(self, potenciometro, comando):
        self._mapa_elementos.get(potenciometro).setValue(comando)
    def actualizarProgramas(self, lista_programas : list):
        for combo in self.combos:
            actual = combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(lista_programas)
            if actual in lista_programas:
                combo.setCurrentText(actual)
            else:
                combo.setCurrentIndex(-1)
            combo.blockSignals(False)
    def getProgramaPot(self, potenciometro : str):
        return "asd"
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
            if isinstance(elemento, QTextEdit):
                elemento.append(senial[1])

        else:
            pass
            ##mandar una advertencia que no se encontro ese elemento

    def mostrar(self):
        self.show()