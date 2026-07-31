from PyQt6.QtWidgets import QLabel,QWidget,QVBoxLayout, QHBoxLayout,QLineEdit, QPushButton, QButtonGroup, QColorDialog
from PyQt6.QtCore import Qt, QRectF, QRegularExpression
from PyQt6.QtGui import QColor, QPainter, QIcon,QRegularExpressionValidator

from colors import colors
from Components.customWidgets import SegmentedButton

class TextEditor(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.selectedColor = QColor("#FF99FF")
        self.controller = controller
        self.layout = QVBoxLayout(self)
        self.setObjectName("textEditor")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.panelTitle = QLabel(text="Text Editor")
        self.panelTitle.setObjectName("panelTitle")
        self.layout.addWidget(self.panelTitle)

        self.textRow = QWidget()
        self.textRowLayout = QHBoxLayout(self.textRow)
        self.layout.addWidget(self.textRow)
        self.layout.setAlignment(self.textRow, Qt.AlignmentFlag.AlignTop)

        self.textRowLayout.addWidget(QLabel(text="Text"))
        
        self.textEntry = QLineEdit()
        self.textRowLayout.addWidget(self.textEntry)
        self.textEntry.setText("Hello World")
        self.textEntry.setFixedHeight(33)
        self.textEntry.textChanged.connect(self.onType)
        self.textEntry.setMaxLength(60)
        regex = QRegularExpression(r"^[\x00-\x7F]*$")
        validator = QRegularExpressionValidator(regex)
        self.textEntry.setValidator(validator)

        self.characterCounter = QLabel(text=f"{len(self.textEntry.text())}/60")
        self.textRowLayout.addWidget(self.characterCounter)
        
        modeContainer = QWidget()
        modeContainerLayout = QHBoxLayout(modeContainer)
        self.layout.addWidget(modeContainer)
        modeContainer.setObjectName("modeContainer")

        self.colorModeSelector = SegmentedButton(values=["Solid","Rainbow"])
        self.colorModeSelector.buttonGroup.idClicked.connect(self.handleColorMode)
        modeContainerLayout.addWidget(self.colorModeSelector)

        self.colorRow = QWidget()
        self.colorRowLayout = QHBoxLayout(self.colorRow)
        self.layout.addWidget(self.colorRow)
        self.layout.setAlignment(self.colorRow,Qt.AlignmentFlag.AlignTop)

        self.colorRowLayout.addWidget(QLabel(text="Text color"))

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


        self.layout.addStretch()

        self.setStyleSheet(f"""
            *{{
                color:{colors['text']};
                border-radius: 10px;
                padding:1px;
                margin:0px;
                height:20px;
            }}
            #textEditor{{
                background-color: {colors['bg-light']};
                margin:0;
                padding:2px;
                border: 1px solid {colors['border']};
            }}
            QLineEdit{{
                border: 1px solid {colors['border']};
                background-color:{colors['bg-light']}
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
            #modeContainer{{
                background-color:{colors['bg-dark']};
            }}
            #panelTitle{{
                font-size:24px;
            }}
        """)
    
    def onType(self):
        self.characterCounter.setText(f"{len(self.textEntry.text())}/60")
        self.controller.setText(self.textEntry.text())
    
    def handleColorMode(self):
        value = self.colorModeSelector.getValue()
        self.controller.setTextColor(mode=value)
        if value == "Rainbow":
            self.colorRow.setHidden(True)
        else:
            self.colorRow.setHidden(False)

    def handleOpenColorDialog(self):
        self.selectedColor=self.colorDialog.getColor(self.selectedColor)
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
        rgb = self.selectedColor.getRgb()
        self.controller.setColor(rgb[0],rgb[1],rgb[2])