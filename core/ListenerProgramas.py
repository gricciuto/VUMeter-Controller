from collections import deque
from queue import Queue

import wmi
from threading import Thread

from PySide6.QtCore import QObject, Signal


class ListenerProgramas(QObject):
    senial_programa = Signal()
    def __init__(self):
        super().__init__()

    def _watch_creation(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("creation")
        while True:
            avisador()
            self.senial_programa.emit()
            #print("Se notifico apertura")
    def _watch_deletion(self):
        w = wmi.WMI()
        avisador = w.Win32_Process.watch_for("deletion")
        while True:
            avisador()
            #print("Se notifico cierre")
            self.senial_programa.emit()

    def listen(self):
        Thread(target=self._watch_creation, daemon=True).start()
        Thread(target=self._watch_deletion, daemon=True).start()
