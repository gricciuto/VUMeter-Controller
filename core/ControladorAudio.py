import threading
from collections import deque

import soundcard
import numpy as np
import time



class ControladorAudio(threading.Thread):

    microfonos = None
    disp_captura = None

    detener = False
    def __init__(self, cola : deque):
        self.microfonos = soundcard.all_microphones(include_loopback=True)
        self.cola = cola
        super().__init__(daemon=True)


    def getMicrofonos(self):
        return self.microfonos
    def setDispCaptura(self, microfono):
        for item in self.microfonos:
            if item.name == microfono:
                self.disp_captura = item
    def stop(self):
        self.detener = True
    def run(self):

        with self.disp_captura.recorder(samplerate=44100, channels=2, blocksize=4096) as recorder:
            while True:
                if self.detener:
                    self.detener = False
                    break
                datos = recorder.record(numframes=2048)

                rms_der = np.sqrt(np.mean(datos[:, 1] ** 2)) * 0.8
                rms_izq = np.sqrt(np.mean(datos[:, 0] ** 2)) * 0.8

                db_der = 20 * np.log10(rms_der + 1e-6)
                db_izq = 20 * np.log10(rms_izq + 1e-6)

                nivel_der = np.clip((db_der + 40) / 40, 0, 1)
                nivel_izq = np.clip((db_izq + 40) / 40, 0, 1)

                self.cola.append(["NIVELES", nivel_der, nivel_izq] )
                ##self.interfaz.ui.progressBar.setValue(int(nivel_izq*100))
                ##self.interfaz.ui.progressBar_2.setValue(int(nivel_der*100))
                ##pwm_der = int(nivel_der * 255)
                ##pwm_izq = int(nivel_izq * 255)

                ##self.func_enviar(pwm_der, pwm_izq)


                time.sleep(0.03)  # bajé el delay para que sea más fluido

