import sys
from PyQt6 import QtWidgets, QtCore
from interfaz_ui import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(800, 600)
widget.setWindowTitle("Controlador Serial")
widget.show()
exit(app.exec())

