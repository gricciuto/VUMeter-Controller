from abc import ABC,abstractmethod
class AdministradorVolumen(ABC):
    def __init__(self, cola: Queue):
        self.lista_programas = []
        self.cola = cola
    
    @abstractmethod
    def actualizarListaProgramas(self):
        pass
    @abstractmethod
    def actualizarVolumen(self,programa,nivel):
        pass
    @abstractmethod
    def actualizarVolumenMaster(self,nivel):
        pass
