from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from Components.TopBar import TopBar
from Components.BasicsPanel import BasicsPanel

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
        

        self.basicsPanel = BasicsPanel(controller=self.controller)
        self.mainLayout.addWidget(self.basicsPanel)
        self.mainLayout.setAlignment(self.basicsPanel, Qt.AlignmentFlag.AlignTop)
        
        self.mainLayout.addStretch()

        self.setStyleSheet(f"""
            *{{
                margin:0;
            }}
            #mainWindow{{
                background-color:{colors["bg-dark"]}
            }}
        """)

