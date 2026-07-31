from communications import ControllerAPI
from ui import App
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont,QIcon
import sys
import os
import json

def resource_path(relative_path):
    try:base_path = sys._MEIPASS
    except AttributeError:base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def checkForSaveFolder():
    with open("config.json","r") as f:
        data = json.load(f)
    if not os.path.exists(data["savePath"]):
        os.mkdir(data["savePath"])

if __name__ == "__main__":
    checkForSaveFolder()
    controllerInstance = ControllerAPI()
    app = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont(resource_path("fonts/PixelifySans.ttf"))
    font = QFont("Pixelify Sans", 12)
    
    app.setFont(font)
    window = App(controllerInstance)
    window.setWindowIcon(QIcon(resource_path("icons/icon.png")))
    window.setWindowTitle("Matrix manager")
    window.show()
    app.exec()
