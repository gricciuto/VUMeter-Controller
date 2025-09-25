from pycaw.pycaw import AudioUtilities
#Cada potenciometro va a tener su administrador de volumen, el administrador va a poder contestar si tiene un programa asignado o no
class AdministradorVolumenPrograma:
    nombre_programa = None
    interfaz = None
    interfaz_ui = None
    def __init__(self,interfaz_ui): # se le va a pasar el campo de texto que tiene asignado ese potenciometro
        self.interfaz_ui = interfaz_ui
    def asignarPrograma(self, nombre_programa):
        self.nombre_programa = nombre_programa
        sesiones = AudioUtilities.GetAllSessions()
        for sesion in sesiones:
            interfaz = sesion.SimpleAudioVolume
            if sesion.Process and sesion.Process.name() == self.nombre_programa:
                self.interfaz = interfaz #Con esto el objeto ya tendria la interfaz del programa que tiene asignado
                self.interfaz_ui.addItem(self.nombre_programa)
                self.interfaz_ui.setCurrentIndex(0)

    def setVolumen(self, volumen):
        self.interfaz.SetMasterVolume(volumen, None)
    def getPrograma(self):
        return self.nombre_programa
    def removerPrograma(self):
        self.interfaz = None
        self.nombre_programa = None
        self.interfaz_ui.removeItem(self.interfaz_ui.currentIndex())
        self.interfaz_ui.setPlaceholderText("No hay programa seleccionado")
    def tienePrograma(self):
        return self.nombre_programa is not None