import psutil
import time

class ListenerProgramasLinux(ListenerProgramas,QObject):
    procesos_previos = set()
    def __init__(self, cola: Queue):
        self.cola = cola
        self.senialPrograma = Signal()
    def _watch_creation(self):
        while True:
            procesos_actuales = {
                (p.pid, p.name())
                for p in psutil.process_iter(['name'])
            }

            iniciados = procesos_actuales - procesos_previos
            cerrados = procesos_previos - procesos_actuales

            if (iniciados.__len__ != 0 or cerrados.__len__ != 0):
                self.senialPrograma.emit()
                self.cola.put(["EVENTO", "Se creo un programa"])
            procesos_previos = procesos_actuales
            time.sleep(1)
    def _watch_deletion(self):
        pass
    def listen(self):
        Thread(target=self._watch_creation, daemon=True).start()
