import threading
from collections import deque
from queue import Queue

from PySide6.QtCore import Signal, QThread, QObject

from core.AdministradorVolumen import AdministradorVolumen
from core.ControladorAudio import ControladorAudio
from core.Interfaz import Interfaz
from core.SerialArduino import get_puertos, SerialArduino

#Tengo que decirle que hacer al modulo que quiero que haga algo, como lo hace no me importa, solo tengo que avisarle
class EventCoordinator(QThread):


    senial = Signal(list)
    lista_programas = []
    potenciometros = {
        "POT2": None,
        "POT3": None,
        "POT4": None,
        "POT5": None,
        "POT6": None
    }
    def __init__(self,cola : Queue,administradorVolumen : AdministradorVolumen, controladorAudio: ControladorAudio, serialArduino : SerialArduino, interfaz:Interfaz):
        super().__init__()
        self.interfaz = interfaz
        self.interfaz.ui.botonConectar.clicked.connect(self.conectarArduino)
        self.interfaz.ui.botonIniciar.clicked.connect(self.iniciarCaptura)
        self.cola = cola
        self.serialArduino = serialArduino
        self.serialArduino.senial_conectado.connect(self.on_arduinoConectado)
        self.serialArduino.senial_error.connect(self.on_arduinoError)
        self.controladorAudio = controladorAudio

        ## Hilos que se van a usar durante la ejecucion
        self.hiloCaptura = threading.Thread(target=self.controladorAudio.run, daemon=True)

        self.administradorVolumen = administradorVolumen
        self.administradorVolumen.actualizarListaProgramas()
        self.cola.put(["INTERFAZ","COMBOBOX_ARDUINO",get_puertos()])

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
            case "BOTON":
                match senial[1]:
                    case "iniciar":
                        #Cuando se clickea iniciar, se le pide a la interfaz que setee el microfono.
                        self.senial.emit(["GET_MICROFONOS"])
    def conectarArduino(self):
        puerto = self.interfaz.getPuertoSeleccionado()
        self.serialArduino.conectar(puerto)
    def on_arduinoConectado(self):
        self.interfaz.arduinoConectado()
    def on_arduinoError(self):
        self.interfaz.mostrarError("Error conectando con el Arduino")
    def iniciarCaptura(self):
        pass
    #Consumidor de items de la cola
    def run(self):

        while True:
            entrada = self.cola.get(block=True)
            match entrada[0]:
                case "SET_MICROFONO":
                    self.controladorAudio.setDispCaptura(entrada[1])
                    self.hiloCaptura = threading.Thread(target=self.controladorAudio.run, daemon=True)
                    self.hiloCaptura.start()

                case "ARDUINO_CONECTADO":
                    self.senial.emit(["ARDUINO_CONECTADO"])
                    print("Se emitio arduino_conectado")
                case "BORRAR_PROGRAMA":
                    self.lista_programas.remove(entrada[1])
                    self.senial.emit(["LISTA_PROGRAMAS",self.lista_programas])
                case "CREAR_PROGRAMA":
                    self.lista_programas.append(entrada[1])
                    #Si no esta asignado a ningun potenciometro y hay alguno que es none, que se meta de una
                    self.senial.emit(["LISTA_PROGRAMAS",self.lista_programas])

                    #No funciona
                    #if entrada[1] not in self.potenciometros.values():
                    #    for potenciometro,programa in self.potenciometros.items():
                    #        if programa is None:
                    #            self.potenciometros[potenciometro] = entrada[1]
                    #            self.senial.emit([f"COMBOBOX_{potenciometro}", entrada[1]])
                    #            print(self.potenciometros)
                    #            break
                case "POT1":
                    #Se emite la senial para que la interfaz actualice el potenciometro
                    self.senial.emit(["SLIDER_MASTER",entrada[1]])
                    #self.administradorVolumen.actualizarVolumenMaster(entrada[1])
                case "POT2":
                    self.senial.emit(["SLIDER_POT1", entrada[1]])
                    #self.administradorVolumen.actualizarVolumen(self.potenciometros.get("POT2"), entrada[1])
                case "EVENTO":
                    self.administradorVolumen.actualizarListaProgramas()
                    #print(self.lista_programas)
                case "ERROR":
                    print(f"ERROR: {entrada[1]}")
                    self.senial.emit(["LOG",entrada[1]])
                case "INFO":
                    print(f"INFO: {entrada[1]}")
                case "INTERFAZ":
                    self.senial.emit([entrada[1],entrada[2]])
                case "NIVELES":
                    self.serialArduino.enviar(entrada[1],entrada[2])

