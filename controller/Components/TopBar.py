from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
import sys
import os
import threading

from colors import colors

from Components.error import showError

def resource_path(relative_path):
    try:base_path = sys._MEIPASS
    except AttributeError:base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TopBar(QWidget):
    def __init__(self, controller,connectionCallback=None,disconnectionCallback=None):
        super().__init__()
        self.connectionCallback = connectionCallback
        self.disconnectionCallback = disconnectionCallback
        self.controller = controller
        self.layout = QHBoxLayout(self)
        self.setObjectName("topBar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.titleWidget = QWidget()
        self.titleWidget.setFixedWidth(350)
        self.titleWidgetLayout = QHBoxLayout(self.titleWidget)
        self.layout.addWidget(self.titleWidget)
        self.layout.setAlignment(self.titleWidget,Qt.AlignmentFlag.AlignLeft)

        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon.setFixedSize(50,50)
        self.iconPixmap = QPixmap(resource_path("icons/icon.png"))
        self.iconPixmapScaled = self.iconPixmap.scaled(self.icon.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(self.iconPixmapScaled)
        self.titleWidgetLayout.addWidget(self.icon)

        title = QLabel(text="Matrix manager")
        title.setObjectName("title")
        self.titleWidgetLayout.addWidget(title)

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

        self.connectButton = QPushButton(text="Connect")
        self.selectorContainerLayout.addWidget(self.connectButton)
        self.connectButton.clicked.connect(self.connectButtonAction)

        self.stateDisplayContainer = QWidget()
        self.stateDisplayContainerLayout = QHBoxLayout(self.stateDisplayContainer)
        self.layout.addWidget(self.stateDisplayContainer)
        self.layout.setAlignment(self.stateDisplayContainer,Qt.AlignmentFlag.AlignRight)



        self.sizeLabel = QLabel(text="")
        self.stateDisplayContainerLayout.addWidget(self.sizeLabel)

        self.stateLabel = QLabel(text="Disconnected")
        self.stateDisplayContainerLayout.addWidget(self.stateLabel)



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
                font-size:32px;
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

    def connectButtonAction(self):
        try:
            if self.controller.getStatus()["connected"]:
                self.connectButton.setText("Connect")
                self.controller.disconnect()
                self.stateLabel.setText("Disconnected")
                self.sizeLabel.setText("")
                if self.disconnectionCallback: self.disconnectionCallback()
            else:
                self.controller.connect(self.comboBox.currentText())
                result = self.controller.getStatus()
                if result["connected"]:
                    self.stateLabel.setText("Connected")
                    self.sizeLabel.setText(f"{result['dimensions']['x']}x{result['dimensions']['y']}")
                    self.connectButton.setText("Disconnect")
                    if self.connectionCallback: self.connectionCallback(result['dimensions']['x'],result['dimensions']['y'])
        except Exception as e:
            showError(self,message=str(e))