from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QColorDialog
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QIcon
import sys
import os
import threading

from colors import colors
from Components.customWidgets import SegmentedButton

class PatternEditor(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller
        self.selectedColor = QColor("#FF99FF")
        self.layout = QVBoxLayout(self)
        self.setObjectName("patternEditor")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.panelTitle = QLabel(text="Pattern Editor")
        self.panelTitle.setObjectName("panelTitle")
        self.layout.addWidget(self.panelTitle)

        self.colorRow = QWidget()
        self.colorRowLayout = QHBoxLayout(self.colorRow)
        self.layout.addWidget(self.colorRow)
        self.layout.setAlignment(self.colorRow,Qt.AlignmentFlag.AlignTop)

        self.colorRowLayout.addWidget(QLabel(text="Effect color"))

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



        patternContainer = QWidget()
        patternContainer.setObjectName("patternContainer")
        patternContainerLayout = QHBoxLayout(patternContainer)
        self.layout.setAlignment(patternContainer,Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(patternContainer)

        patterns = ["Rainbow","Checker","Scanner","Pulse","Snake","Rainbow fill"]
        self.patternChooser = SegmentedButton(values=patterns,orientation="vertical")
        self.patternChooser.buttonGroup.idClicked.connect(self.handlePatternSelection)
        patternContainerLayout.addWidget(self.patternChooser)

        self.layout.addStretch()

        self.setStyleSheet(f"""
            *{{
                color:{colors['text']};
                border-radius: 10px;
                padding:1px;
                margin:0px;
                height:20px;
            }}
            #patternEditor{{
                background-color: {colors['bg-light']};
                margin:0;
                padding:2px;
                border: 1px solid {colors['border']};
            }}
            SegmentedButton{{
                background-color:{colors['bg-dark']};
                border: 1px solid {colors['border']};
            }}
            SegmentedButton QPushButton{{
                background-color:transparent;
                border: none;
            }}
            SegmentedButton QPushButton:hover{{
                background-color:{colors['highlight']}
            }}
            SegmentedButton QPushButton:checked{{
                background-color:{colors['primary']};
            }}
            #patternContainer{{
                background-color:{colors['bg-dark']};
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
            #panelTitle{{
                font-size:24px;
            }}
        """)

    def handleOpenColorDialog(self):
        self.selectedColor=self.colorDialog.getColor(self.selectedColor)
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
        rgb = self.selectedColor.getRgb()
        self.controller.setColor(rgb[0],rgb[1],rgb[2])
    
    def handlePatternSelection(self):
        value = self.patternChooser.getValue()
        self.controller.setPattern(value)
        