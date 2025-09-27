from collections import deque

from core.AdministradorVolumenPrograma import AdministradorVolumenPrograma
from pycaw.pycaw import AudioUtilities


#Este modulo se deberia de encargar de obtener una lista de programas y segun la
#orden que reciba del modulo de logica, establecer el volumen de cierto programa a un cierto valor

class AdministradorVolumen:
    #Las variables que se definan aca van a ser variables estaticas de la clase
    def __init__(self, cola : deque):
        self.lista_programas = []
        self.cola = cola

    def actualizarListaProgramas(self):
        sesiones = AudioUtilities.GetAllSessions()
        self.lista_programas.clear()

        for sesion in sesiones:
            if sesion.Process is not None:
                self.lista_programas.append(sesion)
                self.cola.append(["NUEVO_PROGRAMA", sesion.Process.name()])


    def actualizarVolumen(self,programa,nivel):
        for proceso in self.lista_programas:
            if proceso.Process.name == programa:
                proceso.SimpleAudioVolume.SetMasterVolume(nivel, None)
