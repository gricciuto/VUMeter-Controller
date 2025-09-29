from collections import deque
from queue import Queue

from comtypes import CLSCTX_ALL
from pycaw.api.endpointvolume import IAudioEndpointVolume

from core.AdministradorVolumenPrograma import AdministradorVolumenPrograma
from pycaw.pycaw import AudioUtilities


#Este modulo se deberia de encargar de obtener una lista de programas y segun la
#orden que reciba del modulo de logica, establecer el volumen de cierto programa a un cierto valor

class AdministradorVolumen:
    #Las variables que se definan aca van a ser variables estaticas de la clase

    def __init__(self, cola : Queue):
        self.lista_programas = []
        self.cola = cola

    def actualizarListaProgramas(self):
        sesiones = AudioUtilities.GetAllSessions()
        nombres_sesiones = [s.Process.name() for s in sesiones if s.Process is not None]
        for nombre in nombres_sesiones:
            if nombre not in self.lista_programas:
                self.lista_programas.append(nombre)
                self.cola.put(["CREAR_PROGRAMA", nombre])

        for programa in list(self.lista_programas):
            if programa not in nombres_sesiones:
                self.lista_programas.remove(programa)
                self.cola.put(["BORRAR_PROGRAMA", programa])


    def actualizarVolumen(self,programa,nivel):
        for proceso in self.lista_programas:
            if proceso.Process.name == programa:
                proceso.SimpleAudioVolume.SetMasterVolume(nivel, None)

    def actualizarVolumenMaster(self,nivel):
        devices = AudioUtilities.GetSpeakers()
        interfaz = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volumen = interfaz.QueryInterface(IAudioEndpointVolume)
        volumen.SetMasterVolumeLevelScalar(nivel/100, None)

