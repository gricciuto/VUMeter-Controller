import sys
from collections import deque

from PySide6.QtWidgets import QApplication

from core.Interfaz import Interfaz

if __name__ == "__main__":
    bus = deque()

    app = QApplication(sys.argv)
    interfaz = Interfaz()
    interfaz.inicializar()
    interfaz.mostrar()
    sys.exit(app.exec())

