from abc import ABC, abstractmethod

class Paquete (ABC):
    @abstractmethod
    def getPaqueteArduino(self):
        pass
class PaqueteSonido(Paquete):
    def __init__(self, nivelIzquierdo : int, nivelDerecho : int):
        self.nivelIzquierdo = nivelIzquierdo
        self.nivelDerecho = nivelDerecho
    def getPaqueteArduino(self):
        return f"1.{self.nivelIzquierdo * 255},{self.nivelDerecho * 255}\n"
    def getPaqueteInterfaz(self):
        return int(self.nivelIzquierdo * 100), int(self.nivelDerecho * 100)

class PaqueteSaludo(Paquete):
    def getPaqueteArduino(self):
        return "5.hs\n"
    def checkRespuesta(self, respuesta):
        header, comando, checksum = respuesta
        return header == 0xAA and checksum == (header ^ comando)

class PaqueteLuz(Paquete):
    estado = False
    def setEstado(self, estado: bool):
        self.estado = estado
    def getPaqueteArduino(self):
        if self.estado:
            return "2.100\n"
        return "2.0\n"
class PaqueteArduino(Paquete):
    def __init__(self, header, comando, checksum):
        self.header = header
        self.comando = comando
        self.checksum = checksum
        self.mapa_elementos = {
            0xA1 : "SLIDER_MASTER",
            0xA2 : "SLIDER_POT1",
            0xA3 : "SLIDER_POT2",
            0xA4 : "SLIDER_POT3",
            0xA5 : "SLIDER_POT4",
            0xA6 : "SLIDER_POT5",
        }
    def esPaqueteValido(self):
        return self.checksum == (self.header ^ self.comando)
    def getPaqueteArduino(self):
        return self.mapa_elementos.get(self.header), self.comando