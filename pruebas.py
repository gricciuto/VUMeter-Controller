import sys

from PyQt6.QtWidgets import QApplication

from core.Interfaz import Interfaz

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interfaz = Interfaz()
    interfaz.inicializar()
    interfaz.mostrar()
    sys.exit(app.exec())

