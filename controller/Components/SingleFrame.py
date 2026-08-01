from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, QFileDialog, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon
import sys
import os
import json

from colors import colors
from Components.customWidgets import MatrixDisplay
from Components.error import showError

def resource_path(relative_path):
    try:base_path = sys._MEIPASS
    except AttributeError:base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SingleFrameEditor(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.selectedColor = QColor("#FF99FF")
        self.setObjectName("singlePanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layout = QHBoxLayout(self)


        self.controlsWidget = QWidget()
        self.controlsLayout = QVBoxLayout(self.controlsWidget)
        self.controlsWidget.setMaximumWidth(500)
        self.layout.addWidget(self.controlsWidget)

        self.panelTitle = QLabel(text="Single Frame Editor")
        self.panelTitle.setObjectName("panelTitle")
        self.controlsLayout.addWidget(self.panelTitle)

        self.colorRow = QWidget()
        self.colorRowLayout = QHBoxLayout(self.colorRow)
        self.controlsLayout.addWidget(self.colorRow)
        self.controlsLayout.setAlignment(self.colorRow,Qt.AlignmentFlag.AlignTop)

        self.colorRowLayout.addWidget(QLabel(text="Color"))

        self.openDialog = QPushButton(text="Select color")
        self.openDialog.clicked.connect(self.handleOpenColorDialog)
        self.colorRowLayout.addWidget(self.openDialog)

        self.colorDialog = QColorDialog()

        self.colorDisplay = QWidget()
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
        self.colorDisplay.setFixedHeight(33)
        self.colorRowLayout.addWidget(self.colorDisplay)

        self.pickerModeButton = QPushButton(icon=QIcon(resource_path("icons/picker.png")))
        self.pickerModeButton.setCheckable(True)
        self.pickerModeButton.setChecked(False)
        self.pickerModeButton.setFixedWidth(33)
        self.pickerModeButton.clicked.connect(self.handlePickerSelection)
        self.colorRowLayout.addWidget(self.pickerModeButton)
        
        self.fillButton = QPushButton(text="Fill matrix with color")
        self.controlsLayout.addWidget(self.fillButton)
        self.fillButton.clicked.connect(self.handleMatrixFill)
        self.controlsLayout.setAlignment(self.fillButton,Qt.AlignmentFlag.AlignTop)

        self.fileOperationsWidget = QWidget()
        self.fileOperationsWidget.setObjectName("fileOperations")
        self.fileOperationsWidgetLayout = QHBoxLayout(self.fileOperationsWidget)
        self.controlsLayout.addWidget(self.fileOperationsWidget)
        self.controlsLayout.setAlignment(self.fileOperationsWidget,Qt.AlignmentFlag.AlignTop)

        self.frameNameEntry = QLineEdit()
        self.frameNameEntry.setMaximumWidth(350)
        self.frameNameEntry.setPlaceholderText("Image name")
        self.frameNameEntry.setText("Matrix image")
        self.fileOperationsWidgetLayout.addWidget(self.frameNameEntry)

        self.saveButton = QPushButton(text="Save")
        self.saveButton.clicked.connect(self.handleSaveToFile)
        self.fileOperationsWidgetLayout.addWidget(self.saveButton)
        
        self.loadButton = QPushButton(text="Load from file")
        self.loadButton.clicked.connect(self.loadFromFile)
        self.fileOperationsWidgetLayout.addWidget(self.loadButton)
        
        self.controlsLayout.addStretch()

        self.sendButton = QPushButton(text="Send")
        self.sendButton.clicked.connect(self.send)
        self.controlsLayout.addWidget(self.sendButton)



        self.preview = MatrixDisplay()
        self.preview.callback = self.handlePreviewCallback
        self.preview.resizeMatrix(8,8)
        self.layout.addWidget(self.preview)
        
        self.setStyleSheet(f"""
            *{{
                color:{colors['text']};
                border-radius: 10px;
                padding:5px;
                height:20px;
            }}
            #singlePanel{{
                background-color: {colors['bg-light']};
                margin:0;
                padding:2px;
                border: 1px solid {colors['border']};
            }}
            QPushButton{{
                border: 1px solid {colors['border']};
                background-color:{colors['bg-light']}
            }}
            QPushButton:pressed{{
                border-color:{colors['highlight']}
            }}
            QPushButton:hover{{
                background-color:{colors['border-muted']};
            }}
            QPushButton:checked{{
                border-color:{colors['highlight']};
                background-color:{colors['border-muted']};
            }}
            MatrixDisplay{{
                background-color:{colors['bg-light']}
            }}
            QLineEdit{{
                border: 1px solid {colors['border']};
                background-color:{colors['bg-light']}
            }}
            #panelTitle{{
                font-size:24px;
            }}
            #fileOperations{{
                background-color: {colors['bg-dark']};
                margin:0;
                padding:2px;
                border: 1px solid {colors['border']};
            }}
            QFileDialog{{
                    background-color:{colors["bg-light"]}
            }}
            QFileDialog *{{
                background-color:{colors["bg-light"]}
            }}
            QFileDialog QToolButton{{
                border: 1px solid {colors['border']};
            }}
        """)
    
    def handlePickerSelection(self):
        if self.pickerModeButton.isChecked():
            self.preview.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.preview.setCursor(Qt.CursorShape.ArrowCursor)
    
    def handlePreviewCallback(self,x,y):
        try:
            if self.pickerModeButton.isChecked():
                self.selectedColor = self.preview.pixelGrid[y][x]
                self.colorDisplay.setStyleSheet(f"""
                    *{{background-color:rgba{self.selectedColor.getRgb()}}}
                """)
                self.pickerModeButton.setChecked(False)
                self.preview.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                self.preview.pixelGrid[y][x] = self.selectedColor
                self.preview.update()
                rgb = self.selectedColor.getRgb()
                self.controller.setPixel(x,y,rgb[0],rgb[1],rgb[2])
        except Exception as e:
            showError(self,str(e))
    
    def handleMatrixFill(self):
        self.preview.pixelGrid = [[self.selectedColor for a in range(len(self.preview.pixelGrid[0]))] for b in range(len(self.preview.pixelGrid))]
        self.preview.update()
        rgb = self.selectedColor.getRgb()
        self.controller.setColor(rgb[0],rgb[1],rgb[2])
        self.controller.fillWithColor()
    
    def handleOpenColorDialog(self):
        self.selectedColor=self.colorDialog.getColor(self.selectedColor)
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
    
    def resizeMatrix(self,w,h):
        self.preview.resizeMatrix(w,h)
    
    def send(self):
        for y in range(len(self.preview.pixelGrid)):
            for x in range(len(self.preview.pixelGrid[0])):
                rgb = self.preview.pixelGrid[y][x].getRgb()
                self.controller.setPixel(x,y,rgb[0],rgb[1],rgb[2])

    def loadFromFile(self):
        try:
            with open("config.json","r") as f: config = json.load(f)
            filenameDialog = QFileDialog(filter=".json")
            filename = filenameDialog.getOpenFileName(self,"Load matrix",config["savePath"])
            if not filename[0]: return
            if not os.path.exists(filename[0]): raise FileNotFoundError("File doesn't seem to exist!")
            with open(filename[0],"r") as f: data=json.load(f)
            if data.get("type") != "single": raise ValueError("Invalid json file, file doens't contain a single frame!")
            self.frameNameEntry.setText(data.get("name","noname"))
            self.selectedColor = QColor("black")
            self.handleMatrixFill()
            for y in range(min(len(self.preview.pixelGrid),data["gridHeight"])):
                for x in range(min(len(self.preview.pixelGrid[0]),data["gridHeight"])):
                    self.selectedColor = QColor(data["frame"][y][x][0],data["frame"][y][x][1],data["frame"][y][x][2])
                    self.preview.pixelGrid[y][x] = self.selectedColor
                    self.preview.update()
                    self.controller.setPixel(x,y,data["frame"][y][x][0],data["frame"][y][x][1],data["frame"][y][x][2])
        except Exception as e:
            showError(self,str(e))

    def handleSaveToFile(self):
        try:
            with open("config.json","r") as f: config = json.load(f)
            filenameDialog = QFileDialog(filter=".json")
            filename = filenameDialog.getSaveFileName(self,"Save matrix",os.path.join(config["savePath"],f"{self.frameNameEntry.text()}.json"))
            filename = filename[0]
            if not filename: raise ValueError("can't save to empty filename!")
            colorFrame=[[(0,0,0) for i in range(len(self.preview.pixelGrid[0]))] for y in range(len(self.preview.pixelGrid))]

            for y in range(len(self.preview.pixelGrid)):
                for x in range(len(self.preview.pixelGrid[0])):
                    qcolorObject = self.preview.pixelGrid[y][x]
                    colorTouple = qcolorObject.getRgb()
                    colorFrame[y][x] = (colorTouple[0],colorTouple[1],colorTouple[2])
            data = {
                "name":self.frameNameEntry.text(),
                "type":"single",
                "gridWidth":len(self.preview.pixelGrid[0]),
                "gridHeight":len(self.preview.pixelGrid),
                "frame":colorFrame
            }
            with open(filename,"w") as f:
                json.dump(data,f,indent=4)
        except Exception as e:
            showError(self,str(e))