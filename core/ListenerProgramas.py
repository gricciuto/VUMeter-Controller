from collections import deque

import wmi
from threading import Thread

class ListenerProgramas:
    def __init__(self, cola: deque):
        self.cola = cola

    def _watch_creation(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("creation")
        while True:
            avisador()
            print("se creo un programa")
            self.cola.append(["EVENTO","Se creo un programa"])

    def _watch_deletion(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("deletion")
        while True:
            avisador()
            print("se borro un programa")
            self.cola.append(["EVENTO","Se borro un programa"])

    def listen(self):
        Thread(target=self._watch_creation, daemon=True).start()
        Thread(target=self._watch_deletion, daemon=True).start()
