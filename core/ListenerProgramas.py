from abc import ABC,abstractmethod

class ListenerProgramas(ABC):
    @abstractmethod
    def _watch_creation(self):
        pass
    @abstractmethod
    def _watch_deletion(self):
        pass
    @abstractmethod
    def listen(self):
        pass