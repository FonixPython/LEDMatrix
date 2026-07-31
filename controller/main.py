from communications import ControllerAPI
from ui import App
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase, QFont
import sys
import os
import json

def checkForSaveFolder():
    with open("config.json","r") as f:
        data = json.load(f)
    if not os.path.exists(data["savePath"]):
        os.mkdir(data["savePath"])

if __name__ == "__main__":
    checkForSaveFolder()
    controllerInstance = ControllerAPI()
    app = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont("fonts/PixelifySans.ttf")
    font = QFont("Pixelify Sans", 12)
    
    app.setFont(font)
    window = App(controllerInstance)
    window.show()
    app.exec()
