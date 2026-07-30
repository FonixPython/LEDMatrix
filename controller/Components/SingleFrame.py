from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QColorDialog
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QIcon
import sys
import os
import threading

from colors import colors
from Components.customWidgets import MatrixDisplay

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
        self.layout.addWidget(self.controlsWidget)

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
        self.controlsLayout.addStretch()


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
        """)
    
    def handlePickerSelection(self):
        if self.pickerModeButton.isChecked():
            self.preview.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.preview.setCursor(Qt.CursorShape.ArrowCursor)
    
    def handlePreviewCallback(self,x,y):
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
            threading.Thread(target=lambda:self.actionColorPixel(x,y)).start()
    def handleMatrixFill(self):
        self.preview.pixelGrid = [[self.selectedColor for a in range(len(self.preview.pixelGrid[0]))] for b in range(len(self.preview.pixelGrid))]
        self.preview.update()
        threading.Thread(target=self.actionFillColor).start()
    def actionFillColor(self):
        rgb = self.selectedColor.getRgb()
        self.controller.setColor(rgb[0],rgb[1],rgb[2])
        self.controller.fillWithColor()
    def actionColorPixel(self,x,y):
        rgb = self.selectedColor.getRgb()
        self.controller.setPixel(x,y,rgb[0],rgb[1],rgb[2])
    def handleOpenColorDialog(self):
        self.selectedColor=self.colorDialog.getColor(self.selectedColor)
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
    def resizeMatrix(self,w,h):
        self.preview.resizeMatrix(w,h)