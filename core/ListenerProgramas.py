import wmi
from threading import Thread

class ListenerProgramas:
    def __init__(self, funcion):
        self.funcion = funcion

    def _watch_creation(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("creation")
        while True:
            proceso_nuevo = avisador()
            print("se creo un programa")
            self.funcion()

    def _watch_deletion(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("deletion")
        while True:
            proceso_terminado = avisador()
            print("se borro un programa")
            self.funcion()

    def listener(self):
        Thread(target=self._watch_creation, daemon=True).start()
        Thread(target=self._watch_deletion, daemon=True).start()
