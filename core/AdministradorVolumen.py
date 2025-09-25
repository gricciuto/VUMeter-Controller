from core.AdministradorVolumenPrograma import AdministradorVolumenPrograma
from pycaw.pycaw import AudioUtilities

class AdministradorVolumen:
    #Las variables que se definan aca van a ser variables estaticas de la clase
    def __init__(self, interfaz):
        #Las variables que se definan aca son de instancias
        self.interfaz = interfaz #la ui que tiene todos los campos de texto de los potenciometros
        self.pot1 = AdministradorVolumenPrograma(interfaz.ui.comboBoxPot1)
        self.pot2 = AdministradorVolumenPrograma(interfaz.ui.comboBoxPot2)
        self.pot3 = AdministradorVolumenPrograma(interfaz.ui.comboBoxPot3)
        self.pot4 = AdministradorVolumenPrograma(interfaz.ui.comboBoxPot4)
        self.pot5 = AdministradorVolumenPrograma(interfaz.ui.comboBoxPot5)
        self.lista_pot = {self.pot1,self.pot2,self.pot3,self.pot4,self.pot5}
        self.lista_programas_asignados = []
        self.lista_programas = []

    def actualizarListaProgramas(self):
        sesiones = AudioUtilities.GetAllSessions()
        self.lista_programas.clear()
        for sesion in sesiones:
            if sesion.Process is not None and not self.lista_programas.__contains__(sesion.Process.name()):
                self.lista_programas.append(sesion.Process.name())
        print("Lista de programas: ")
        print(self.lista_programas)
        self.actualizarPots()

    def actualizarPots(self):
        for pot in self.lista_pot:
            if pot.tienePrograma() and pot.getPrograma() not in self.lista_programas:
                self.lista_programas_asignados.remove(pot.getPrograma())
                pot.removerPrograma()
                print("se borro de la lista")
            for programa in self.lista_programas:
                if programa not in self.lista_programas_asignados and not pot.tienePrograma():
                    self.lista_programas_asignados.append(programa)
                    pot.asignarPrograma(programa)






