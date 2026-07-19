from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from Components.TopBar import TopBar

from colors import colors

class App(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.setObjectName("mainWindow")
        self.controller = controller
        
        self.mainLayout = QVBoxLayout(self)

        self.topBar = TopBar(controller=self.controller)
        self.mainLayout.addWidget(self.topBar)
        self.mainLayout.setAlignment(self.topBar, Qt.AlignmentFlag.AlignTop)

        self.setStyleSheet(f"""
            #mainWindow{{
                background-color:{colors["bg-dark"]}
            }}
        """)

