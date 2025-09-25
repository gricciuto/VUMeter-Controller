import time
from threading import Thread
from pycaw.pycaw import AudioUtilities

from core.AdministradorVolumen import AdministradorVolumen
from core.AdministradorVolumenPrograma import AdministradorVolumenPrograma
from core.ListenerProgramas import ListenerProgramas


#La idea del programa es que por cada aplicacion que haya se cree un objeto el cual se va usar para controlar el volumen de esa misma aplicacion, se van a crear hasta 5 que es la
#cantidad de potenciometros que soporta el arduino, ademas del volumen maestro.


def main():
    adm = AdministradorVolumen(None)
    listener = ListenerProgramas(adm.actualizarListaProgramas)
    Thread(target=listener.listener(), daemon=True).start()
if __name__ == '__main__':
    main()
