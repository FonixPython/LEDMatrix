import sys
import os
from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from colors import colors


def resource_path(relative_path):
    try:base_path = sys._MEIPASS
    except AttributeError:base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TopBar(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.layout = QHBoxLayout(self)
        self.setObjectName("topBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # App title ??
        title = QLabel(text="Matrix manager")
        title.setObjectName("title")
        self.layout.addWidget(title)

        # Selector section
        self.selectorContainer = QWidget()
        self.selectorContainerLayout = QHBoxLayout(self.selectorContainer)
        self.layout.addWidget(self.selectorContainer)
        self.layout.setAlignment(self.selectorContainer, Qt.AlignmentFlag.AlignHCenter)

        refreshButton = QPushButton(icon=QIcon(resource_path("icons/refresh.png")))
        refreshButton.clicked.connect(self.refreshOptions)
        self.selectorContainerLayout.addWidget(refreshButton)



        self.comboBox = QComboBox()
        self.selectorContainerLayout.addWidget(self.comboBox)

        connectButton = QPushButton(text="Connect")
        self.selectorContainerLayout.addWidget(connectButton)
        

        self.stateDisplayContainer = QWidget()
        self.stateDisplayContainerLayout = QHBoxLayout(self.stateDisplayContainer)
        self.layout.addWidget(self.stateDisplayContainer)
        self.layout.setAlignment(self.stateDisplayContainer,Qt.AlignmentFlag.AlignRight)


        self.stateLabel = QLabel(text="Disconnected")
        self.stateDisplayContainerLayout.addWidget(self.stateLabel)

        self.sizeLabel = QLabel(text="")
        self.stateDisplayContainerLayout.addWidget(self.sizeLabel)


        self.setStyleSheet(f"""
            *{{
                color:{colors['text']};
                border-radius: 10px;
                padding:5px;
                height:20px;
            }}
            #topBar{{
                background-color: {colors['bg']};
                margin:0;
                padding:2px;
            }}
            #title{{
                font-size:24px;
            }}
            QComboBox{{
                width:100px;
                border: 1px solid {colors['border']};
                background-color:{colors['bg-light']}
            }}
            QComboBox:hover{{
                background-color:{colors['border-muted']};
            }}
            QComboBox::drop-down{{
                border-radius:0px;
                padding:2px;
                color: {colors['text']};
            }}
            QComboBox::down-arrow{{
                image: url(icons/dropdown.png);
            }}
            QComboBox QAbstractItemView{{
                background-color:{colors["bg-light"]};
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
        """)

        self.refreshOptions()

    def refreshOptions(self):
        devices = self.controller.getDevices()
        self.comboBox.clear()
        for i in devices:
            self.comboBox.addItem(f"{i['device']}")