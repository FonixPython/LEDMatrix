from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from Components.customWidgets import SegmentedButton
from colors import colors


class BasicsPanel(QWidget):
    def __init__(self,controller,changeModeCallback):
        super().__init__()
        self.controller = controller
        self.changeModeCallback = changeModeCallback
        self.layout = QVBoxLayout(self)
        self.setObjectName("basicsPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.brightnessContainer = QWidget()
        self.brightnessContainerLayout = QHBoxLayout(self.brightnessContainer)
        self.layout.addWidget(self.brightnessContainer)

        self.brightnessContainerLayout.addWidget(QLabel(text="Brightness"))
        
        self.brightnessSlider = QSlider(orientation=Qt.Orientation.Horizontal)
        self.brightnessContainerLayout.addWidget(self.brightnessSlider)
        self.brightnessSlider.setMinimum(0)
        self.brightnessSlider.setMaximum(255)
        self.brightnessSlider.setSingleStep(1)
        self.brightnessSlider.setPageStep(10)
        self.brightnessSlider.setValue(self.controller.brightness)
        self.brightnessSlider.valueChanged.connect(self.brightnessSliderChanged)
        self.brightnessSlider.sliderReleased.connect(self.brightnessSliderLetGo)

        self.brightnessLabel = QLabel(text=f"{int(self.brightnessSlider.value()/255*100)}%")
        self.brightnessContainerLayout.addWidget(self.brightnessLabel)
        self.brightnessContainerLayout.setAlignment(self.brightnessLabel,Qt.AlignmentFlag.AlignRight)
        self.brightnessLabel.setFixedSize(65,30)

        self.speedContainer = QWidget()
        self.speedContainerLayout = QHBoxLayout(self.speedContainer)
        self.layout.addWidget(self.speedContainer)
        
        self.speedContainerLayout.addWidget(QLabel(text="Speed"))

        self.speedSlider = QSlider(orientation=Qt.Orientation.Horizontal)
        self.speedContainerLayout.addWidget(self.speedSlider)
        self.speedSlider.setMaximum(1000)
        self.speedSlider.setMinimum(0)
        self.speedSlider.setSingleStep(1)
        self.speedSlider.setPageStep(10)
        self.speedSlider.setValue(100)
        self.speedSlider.setValue(self.controller.speed)
        self.speedSlider.valueChanged.connect(self.speedSliderChange)
        self.speedSlider.sliderReleased.connect(self.speedSliderLetGo)

        self.speedLabel = QLabel(text=str(self.speedSlider.value())+" ms")
        self.speedContainerLayout.setAlignment(self.speedLabel,Qt.AlignmentFlag.AlignRight)
        self.speedContainerLayout.addWidget(self.speedLabel)
        self.speedLabel.setFixedSize(65,30)


        self.modeContainer = QWidget()
        self.modeContainer.setObjectName("modeContainer")
        self.modeContainerLayout = QHBoxLayout(self.modeContainer)
        self.layout.addWidget(self.modeContainer)

        self.modeContainerLayout.addWidget(QLabel(text="Mode"))
        
        match self.controller.mode:
            case "Single": modeIndex = 0
            case "Pattern": modeIndex = 1
            case "Animation": modeIndex = 2
            case "Text": modeIndex = 3
        self.modeSegmented = SegmentedButton(["Single","Pattern","Animation","Text"],default_index=modeIndex)
        self.modeSegmented.setFixedHeight(40)
        self.modeContainerLayout.addWidget(self.modeSegmented)
        self.modeSegmented.buttonGroup.idClicked.connect(self.modeChanged)

        self.setStyleSheet(f"""
            *{{
                color:{colors['text']};
                border-radius: 10px;
                padding:1px;
                margin:0px;
                height:20px;
            }}
            #basicsPanel{{
                background-color: {colors['bg-light']};
                margin:0;
                padding:2px;
                border: 1px solid {colors['border']};
            }}
            QSlider{{
                border-radius: 15px;
                color:{colors['primary']};
            }}
            QSlider::groove {{
                border: 1px solid {colors['border']};
                border-radius: 5px;
                height: 10px; 
                background-color: {colors['bg-light']};
                margin: 2px 0;
            }}
            QSlider::sub-page{{
                border-radius: 5px;
                height: 10px; 
                background-color:{colors['highlight']};
                margin: 2px 0;
            }}
            QSlider::handle{{
                background-color:{colors['primary']};
                border: 0px solid transparent;
                border-radius: 10px;
                width: 20px;
                height: 20px;
                margin: -5px 0px; 
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
            #modeContainer{{
                background-color:{colors['bg-dark']};
            }}
        """)

    def speedSliderChange(self):
        self.speedLabel.setText(f"{self.speedSlider.value()} ms")
    def brightnessSliderChanged(self):
        self.brightnessLabel.setText(f"{int(self.brightnessSlider.value()/255*100)}%")
    def modeChanged(self):
        value = self.modeSegmented.getValue()
        match value:
            case "Single": modeIndex = 0
            case "Pattern": modeIndex = 1
            case "Animation": modeIndex = 2
            case "Text": modeIndex = 3
        self.controller.setMode(value)
        self.changeModeCallback(modeIndex)
    def brightnessSliderLetGo(self):
        self.controller.setBrightness(self.brightnessSlider.value())
    def speedSliderLetGo(self):
        self.controller.setSpeed(self.speedSlider.value())