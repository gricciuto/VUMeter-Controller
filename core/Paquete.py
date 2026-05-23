

class PaqueteSonido:
    def __init__(self, nivelIzquierdo : int, nivelDerecho : int):
        self.nivelIzquierdo = nivelIzquierdo
        self.nivelDerecho = nivelDerecho
    def getPaqueteArduino(self):
        return f"1.{self.nivelIzquierdo * 255},{self.nivelDerecho * 255}\n"
    def getPaqueteInterfaz(self):
        return int(self.nivelIzquierdo * 100), int(self.nivelDerecho * 100)