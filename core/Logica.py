import threading
from collections import deque
from queue import Queue

from PySide6.QtCore import Signal, QThread, QObject


class Logica(QThread,QObject):
    senial = Signal(list)
    lista_programas = []
    potenciometros = {
        "POT2": None,
        "POT3": None,
        "POT4": None,
        "POT5": None,
        "POT6": None
    }
    def __init__(self,cola: Queue,administradorVolumen):
        super().__init__()
        self.cola = cola
        self.administradorVolumen = administradorVolumen
        self.administradorVolumen.actualizarListaProgramas()

    def actualizar(self,senial):
        match senial[0]:
            case "comboBoxPot1":
                self.potenciometros["POT2"] = senial[1]
                print(self.potenciometros)
            case "comboBoxPot2":
                self.potenciometros["POT3"] = senial[1]
                print(self.potenciometros)
            case "comboBoxPot3":
                self.potenciometros["POT4"] = senial[1]
                print(self.potenciometros)
            case "comboBoxPot4":
                self.potenciometros["POT5"] = senial[1]
                print(self.potenciometros)
            case "comboBoxPot5":
                self.potenciometros["POT6"] = senial[1]
                print(self.potenciometros)


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
                    self.administradorVolumen.actualizarVolumenMaster(entrada[1])
                    print(entrada[1])
                case "POT2":

                    self.senial.emit(["SLIDER_POT1", entrada[1]])
                    self.administradorVolumen.actualizarVolumen(self.potenciometros.get("POT2"), entrada[1])
                case "EVENTO":
                    self.administradorVolumen.actualizarListaProgramas()
                    print(self.lista_programas)
