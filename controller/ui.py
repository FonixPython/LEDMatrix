from PyQt6.QtWidgets import QWidget, QVBoxLayout,QStackedWidget,QSizePolicy
from PyQt6.QtCore import Qt
from Components.TopBar import TopBar
from Components.BasicsPanel import BasicsPanel

from Components.SingleFrame import SingleFrameEditor
from Components.Pattern import PatternEditor
from Components.Text import TextEditor
from Components.Animation import AnimationEditor

from colors import colors

class App(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.setObjectName("mainWindow")
        self.controller = controller
        
        self.mainLayout = QVBoxLayout(self)

        self.topBar = TopBar(controller=self.controller,connectionCallback=self.onConnection,disconnectionCallback=self.onDissconnection)
        self.mainLayout.addWidget(self.topBar)
        self.mainLayout.setAlignment(self.topBar, Qt.AlignmentFlag.AlignTop)


        self.basicsPanel = BasicsPanel(controller=self.controller,changeModeCallback=self.onModeChange,speedCallback=self.onSpeedChange)
        self.basicsPanel.setVisible(False)
        self.mainLayout.addWidget(self.basicsPanel)
        self.mainLayout.setAlignment(self.basicsPanel, Qt.AlignmentFlag.AlignTop)

        self.modeStackedWidget = QStackedWidget()
        self.modeStackedWidget.setVisible(False)
        self.modeStackedWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.mainLayout.addWidget(self.modeStackedWidget)
        

        self.singleFramePanel = SingleFrameEditor(controller=self.controller)
        self.singleFramePanel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.modeStackedWidget.addWidget(self.singleFramePanel)
        
        self.patternPanel = PatternEditor(controller=self.controller)
        self.modeStackedWidget.addWidget(self.patternPanel)

        self.animationPanel = AnimationEditor(controller=self.controller,basicsPanel=self.basicsPanel)
        self.modeStackedWidget.addWidget(self.animationPanel)

        self.textPanel = TextEditor(controller=self.controller)
        self.modeStackedWidget.addWidget(self.textPanel)

        self.setStyleSheet(f"""
            *{{
                margin:0;
            }}
            #mainWindow{{
                background-color:{colors["bg-dark"]}
            }}
        """)
    
    def onConnection(self,x,y):
        self.basicsPanel.setVisible(True)
        self.modeStackedWidget.setVisible(True)
        self.singleFramePanel.resizeMatrix(x,y)
        self.animationPanel.resizeMatrix(x,y)
    
    def onDissconnection(self):
        self.basicsPanel.setVisible(False)
        self.modeStackedWidget.setVisible(False)
        self.modeStackedWidget.setCurrentIndex(0)
        

    def onModeChange(self,modeIndex):
        self.modeStackedWidget.setCurrentIndex(modeIndex)
    
    def onSpeedChange(self,speed):
        self.animationPanel.speed = speed
        self.animationPanel.playTimer.setInterval(speed)