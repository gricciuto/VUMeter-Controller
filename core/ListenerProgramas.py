from collections import deque
from queue import Queue

import wmi
from threading import Thread

class ListenerProgramas:
    def __init__(self, cola: Queue):
        self.cola = cola

    def _watch_creation(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("creation")
        while True:
            avisador()
            self.cola.put(["EVENTO","Se creo un programa"])
            print("Se notifico apertura")
    def _watch_deletion(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("deletion")
        while True:
            avisador()
            print("Se notifico cierre")
            self.cola.put(["EVENTO","Se borro un programa"])

    def listen(self):
        Thread(target=self._watch_creation, daemon=True).start()
        Thread(target=self._watch_deletion, daemon=True).start()
