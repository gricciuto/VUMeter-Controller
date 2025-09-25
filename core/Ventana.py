import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from interfaz_ui import Ui_MainWindow

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def mostrarTexto(self, texto):
        self.ui.textEdit.setText(texto + "/n")

    def crearVentana(self):
        app = QApplication(sys.argv)
        window = VentanaPrincipal()
        window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())