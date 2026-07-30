from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QColorDialog
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QIcon
import sys
import os
import threading

from colors import colors
from Components.customWidgets import MatrixDisplay,ColorCard

def resource_path(relative_path):
    try:base_path = sys._MEIPASS
    except AttributeError:base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AnimationEditor(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.layout = QHBoxLayout(self)
        self.selectedColor = QColor("#FF99FF")
        self.selectedColorIndex = 0

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("animationPanel")

        self.animationObject = {
            "palette":[QColor("black"),QColor("red"),QColor("green"),QColor("blue"),QColor("yellow"),QColor("magenta"),QColor("cyan"),QColor("white"),QColor("#FF9911"),QColor("#00FF88")],
            "frames":[]
        }

        # Left side

        self.leftSide = QWidget()
        self.leftSideLayout = QVBoxLayout(self.leftSide)
        self.layout.addWidget(self.leftSide)

        self.colorRow = QWidget()
        self.colorRowLayout = QHBoxLayout(self.colorRow)
        self.leftSideLayout.addWidget(self.colorRow)
        self.leftSideLayout.setAlignment(self.colorRow,Qt.AlignmentFlag.AlignTop)

        self.colorRowLayout.addWidget(QLabel(text="Color"))

        self.openDialog = QPushButton(text="Select color")
        self.openDialog.clicked.connect(self.handleOpenColorDialog)
        self.colorRowLayout.addWidget(self.openDialog)

        self.colorDialog = QColorDialog()

        self.colorDisplay = QWidget()
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.animationObject['palette'][self.selectedColorIndex].getRgb()}}}
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
        self.leftSideLayout.addWidget(self.fillButton)
        self.fillButton.clicked.connect(self.handleMatrixFill)
        self.leftSideLayout.setAlignment(self.fillButton,Qt.AlignmentFlag.AlignTop)

        self.colorRack = QWidget()
        self.colorRack.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.colorRack.setObjectName("colorRack")
        self.colorRackLayout = QVBoxLayout(self.colorRack)
        self.leftSideLayout.addWidget(self.colorRack)

        self.colorRackButtonGroup = QButtonGroup(self)
        self.colorRackButtonGroup.setExclusive(True)
        self.colorRackButtonGroup.idClicked.connect(self.handlePaletteSelection)

        self.cards = []
        for i in range(10):
            card = ColorCard(str(i+1),color=self.animationObject["palette"][i])
            if i == 0: card.setChecked(True)
            self.colorRackButtonGroup.addButton(card)
            self.colorRackLayout.addWidget(card)
            self.cards.append(card)

        self.leftSideLayout.addStretch()


        # Right side

        self.rightSide = QWidget()
        self.rightSideLayout = QVBoxLayout(self.rightSide)
        self.layout.addWidget(self.rightSide)

        self.preview = MatrixDisplay()
        self.preview.callback = self.handlePreviewCallback
        self.preview.resizeMatrix(8,8)
        self.rightSideLayout.addWidget(self.preview)

        self.setStyleSheet(f"""
            *{{
                color:{colors['text']};
                border-radius: 10px;
                padding:5px;
                height:20px;
            }}
            #animationPanel{{
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
            ColorRack{{
                background-color:{colors['bg-dark']};
                border: 1px solid {colors['border']};
            }}
        """)

    def handlePickerSelection(self):
        if self.pickerModeButton.isChecked():
            self.preview.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.preview.setCursor(Qt.CursorShape.ArrowCursor)

    def handleMatrixFill(self):
        self.preview.pixelGrid = [[self.selectedColor for a in range(len(self.preview.pixelGrid[0]))] for b in range(len(self.preview.pixelGrid))]
        self.preview.update()
        rgb = self.selectedColor.getRgb()
        self.controller.setColor(rgb[0],rgb[1],rgb[2])
        self.controller.fillWithColor()

    def handlePreviewCallback(self,x,y):
        if self.pickerModeButton.isChecked():
            self.selectedColor = self.preview.pixelGrid[y][x]
            self.animationObject["palette"][self.selectedColorIndex] = self.selectedColor
            self.cards[self.selectedColorIndex].updateColor(self.selectedColor)
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

    def handleOpenColorDialog(self):
        self.selectedColor=self.colorDialog.getColor(self.selectedColor)
        self.animationObject["palette"][self.selectedColorIndex] = self.selectedColor
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
        self.cards[self.selectedColorIndex].updateColor(self.selectedColor)
    
    def handlePaletteSelection(self):
        self.selectedColorIndex = int(self.colorRackButtonGroup.checkedButton().textData)-1
        self.selectedColor = self.animationObject["palette"][self.selectedColorIndex]
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
    
    def loadFrameToPreview(self,index):
        frame = self.animationObject["frames"][index]
        QcolorFrame = [[self.animationObject["palette"][frame[b][a]] for a in range(len(frame[0]))] for b in range(len(frame))]
        self.preview.pixelGrid = QcolorFrame
        self.preview.update()

    def resizeMatrix(self,w,h):
        self.preview.resizeMatrix(w,h)
        self.animationObject["frames"] = [[]]
        self.animationObject["frames"][0] = [[0 for x in range(w)] for y in range(h)]

