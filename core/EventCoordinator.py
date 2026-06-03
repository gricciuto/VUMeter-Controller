import threading
from collections import deque
from queue import Queue

from PySide6.QtCore import Signal, QThread, QObject

from core.AdministradorVolumen import AdministradorVolumen
from core.ControladorAudio import ControladorAudio
from core.Interfaz import Interfaz
from core.ListenerProgramas import ListenerProgramas
from core.Paquete import PaqueteSonido, Paquete, PaqueteArduino
from core.SerialArduino import get_puertos, SerialArduino
from core.SerialArduinoFake import SerialArduinoFake


#Tengo que decirle que hacer al modulo que quiero que haga algo, como lo hace no me importa, solo tengo que avisarle
class EventCoordinator(QThread):
    senial = Signal(list)
    lista_programas = []

    def __init__(self,cola : Queue,administradorVolumen : AdministradorVolumen, controladorAudio: ControladorAudio, serialArduino : SerialArduino, interfaz: Interfaz, listenerProgramas : ListenerProgramas):
        super().__init__()
        self.interfaz = interfaz
        self.serialArduino = serialArduino
        self.controladorAudio = controladorAudio
        self.listenerProgramas = listenerProgramas
        self.interfaz.ui.botonConectar.clicked.connect(self.conectarArduino)
        self.interfaz.ui.botonIniciar.clicked.connect(self.iniciarCaptura)
        self.interfaz.ui.botonLuz.clicked.connect(self.on_luzClick)
        self.listenerProgramas.senial_programa.connect(self.on_program_change)
        self.cola = cola

        self.serialArduino.senial_conectado.connect(self.on_arduinoConectado)
        self.serialArduino.senial_error.connect(self.on_arduinoError)
        self.serialArduino.senial_info.connect(self.on_arduinoInfo)
        self.serialArduino.senial_potenciometro.connect(self.on_arduinoPotenciometro)
        self.controladorAudio.senial_nivel.connect(self.on_nivelesChanged)



        ## Hilos que se van a usar durante la ejecucion
        self.hiloCaptura = threading.Thread(target=self.controladorAudio.run, daemon=True)

        self.administradorVolumen = administradorVolumen
        self.administradorVolumen.actualizarListaProgramas()
        self.interfaz.actualizarLista(get_puertos(),"COMBOBOX_ARDUINO")
        self.interfaz.actualizarLista(controladorAudio.getMicrofonos(),"COMBOBOX_DISP")

    def actualizar(self,senial):
        match senial[0]:
            case "comboBoxPot1":
                self.potenciometros["POT2"] = senial[1]
                #print(self.potenciometros)
            case "comboBoxPot2":
                self.potenciometros["POT3"] = senial[1]
                #print(self.potenciometros)
            case "comboBoxPot3":
                self.potenciometros["POT4"] = senial[1]
                #print(self.potenciometros)
            case "comboBoxPot4":
                self.potenciometros["POT5"] = senial[1]
                #print(self.potenciometros)
            case "comboBoxPot5":
                self.potenciometros["POT6"] = senial[1]
                #print(self.potenciometros)
    def conectarArduino(self):
        puerto = self.interfaz.getPuertoSeleccionado()
        self.serialArduino.conectar(puerto)
    def on_arduinoConectado(self):
        self.interfaz.arduinoConectado()
    def on_arduinoError(self, detalle):
        self.interfaz.mostrarError("Error conectando con el Arduino: " + detalle )
    def on_arduinoInfo(self, detalle):
        self.interfaz.mostrarInfo(detalle)
    def on_arduinoPotenciometro(self, paquete : PaqueteArduino):
        potenciometro, datos = paquete.getPaqueteArduino()
        self.interfaz.actualizarPotenciometro(potenciometro, datos)
        if potenciometro == "SLIDER_MASTER":
            self.administradorVolumen.actualizarVolumenMaster(datos)
        else:
            self.administradorVolumen.actualizarVolumen(self.interfaz.getProgramaPot(potenciometro), datos)
    def iniciarCaptura(self):
        self.microfono = self.interfaz.getMicronofoSeleccionado()
        self.controladorAudio.setDispCaptura(self.microfono)
        self.controladorAudio.iniciar()
    def on_luzClick(self):
        self.serialArduino.cambiarLuz()
    def on_program_change(self):
        self.administradorVolumen.actualizarListaProgramas()
        self.interfaz.actualizarProgramas(self.administradorVolumen.lista_programas)
    def on_nivelesChanged(self, paquete: PaqueteSonido):
        self.serialArduino.enviar(paquete)
        self.interfaz.setNiveles(paquete)

    #Consumidor de items de la cola
    def run(self):

        while True:
            entrada = self.cola.get(block=True)
            match entrada[0]:

                case "BORRAR_PROGRAMA":
                    self.lista_programas.remove(entrada[1])
                    self.senial.emit(["LISTA_PROGRAMAS",self.lista_programas])
                case "CREAR_PROGRAMA":
                    self.lista_programas.append(entrada[1])
                    #Si no esta asignado a ningun potenciometro y hay alguno que es none, que se meta de una
                    self.senial.emit(["LISTA_PROGRAMAS",self.lista_programas])

                case "POT1":
                    #Se emite la senial para que la interfaz actualice el potenciometro
                    self.senial.emit(["SLIDER_MASTER",entrada[1]])
                    #self.administradorVolumen.actualizarVolumenMaster(entrada[1])
                case "POT2":
                    self.senial.emit(["SLIDER_POT1", entrada[1]])
                    #self.administradorVolumen.actualizarVolumen(self.potenciometros.get("POT2"), entrada[1])

                case "ERROR":
                    print(f"ERROR: {entrada[1]}")
                    self.senial.emit(["LOG",entrada[1]])
                case "INFO":
                    print(f"INFO: {entrada[1]}")



