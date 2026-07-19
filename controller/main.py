from communications import ControllerAPI
from ui import App
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
import sys

if __name__ == "__main__":
    controllerInstance = ControllerAPI()
    app = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont("fonts/PixelifySans.ttf")
    font = QFont("Pixelify Sans", 12)

    app.setFont(font)
    window = App(controllerInstance)
    window.show()
    app.exec()
