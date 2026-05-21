from dataclasses import dataclass
from enum import Enum, auto

class TipoEvento(Enum):
    ERROR = auto()
    INFO = auto()
    NIVELES = auto()

@dataclass
class Evento:
    tipo: TipoEvento
    datos: tuple = ()