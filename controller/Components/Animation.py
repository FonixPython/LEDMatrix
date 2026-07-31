from PyQt6.QtWidgets import QLabel,QWidget,QGridLayout,QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QColorDialog,QFileDialog, QLineEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QIcon
import sys
import os
import time
import json

from colors import colors
from Components.customWidgets import MatrixDisplay,ColorCard,FrameDisplayScroller
from Components.error import showError

def resource_path(relative_path):
    try:base_path = sys._MEIPASS
    except AttributeError:base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AnimationEditor(QWidget):
    def __init__(self,controller,basicsPanel):
        super().__init__()
        self.basicsPanel = basicsPanel
        self.controller = controller
        self.layout = QVBoxLayout(self)
        self.selectedColor = QColor("#FF99FF")
        self.selectedColorIndex = 0
        self.selectedFrameIndex = 0
        self.speed = 100
        self.playTimer = QTimer(self)
        self.playTimer.timeout.connect(self.nextFrame)


        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("animationPanel")

        self.animationObject = {
            "palette":[QColor("black"),QColor("red"),QColor("green"),QColor("blue"),QColor("yellow"),QColor("magenta"),QColor("cyan"),QColor("white"),QColor("#FF9911"),QColor("#00FF88")],
            "frames":[[[0 for a in range(8)] for b in range(8)]]
        }
        self.panelTitle = QLabel(text="Animation Editor")
        self.panelTitle.setObjectName("panelTitle")
        self.layout.addWidget(self.panelTitle)

        self.topWidget = QWidget()
        self.topWidgetLayout = QHBoxLayout(self.topWidget)
        self.layout.addWidget(self.topWidget)

        # Left side

        self.leftSide = QWidget()
        self.leftSideLayout = QVBoxLayout(self.leftSide)
        self.topWidgetLayout.addWidget(self.leftSide)
        self.leftSide.setMaximumWidth(500)


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
        self.colorRack.setObjectName("colorRack")
        self.colorRack.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.colorRackLayout = QGridLayout(self.colorRack)
        self.leftSideLayout.addWidget(self.colorRack)

        self.colorRackButtonGroup = QButtonGroup(self)
        self.colorRackButtonGroup.setExclusive(True)
        self.colorRackButtonGroup.idClicked.connect(self.handlePaletteSelection)

        self.cards = []
        for i in range(10):
            card = ColorCard(str(i+1),color=self.animationObject["palette"][i])
            if i == 0: card.setChecked(True)
            self.colorRackButtonGroup.addButton(card)
            row = 0 if i <= 4 else 1
            column = i if row == 0 else i-5
            self.colorRackLayout.addWidget(card,row,column)
            self.cards.append(card)

        self.leftSideLayout.addStretch()

        # Carousel

        self.animationCarousel = FrameDisplayScroller(self.animationObject,maxFrames=20)
        self.animationCarousel.setMinimumHeight(130)
        self.animationCarousel.buttonGroup.idClicked.connect(self.handleFrameSelection)
        self.leftSideLayout.addWidget(self.animationCarousel)
        self.leftSideLayout.setAlignment(self.animationCarousel,Qt.AlignmentFlag.AlignBottom)

        # Animation controls

        self.animationControlWidget = QWidget()
        self.animationControlWidgetLayout = QHBoxLayout(self.animationControlWidget)
        self.leftSideLayout.addWidget(self.animationControlWidget)
        
        self.frameLabel = QLabel(text=f"{self.selectedFrameIndex+1}/{len(self.animationObject["frames"])}")
        self.frameLabel.setFixedWidth(60)
        self.animationControlWidgetLayout.addWidget(self.frameLabel)

        self.playButton = QPushButton(text="Play")
        self.playButton.setCheckable(True)
        self.playButton.setChecked(False)
        self.playButton.clicked.connect(self.playPause)
        self.animationControlWidgetLayout.addWidget(self.playButton)
        
        self.newBlankButton = QPushButton(text="New blank")
        self.newBlankButton.clicked.connect(self.addBlank)
        self.animationControlWidgetLayout.addWidget(self.newBlankButton)

        self.newDuplicate = QPushButton(text="New duplicate")
        self.newDuplicate.clicked.connect(self.addDuplicate)
        self.animationControlWidgetLayout.addWidget(self.newDuplicate)

        self.deleteFrame = QPushButton(text="Delete")
        self.deleteFrame.setObjectName("deleteButton")
        self.deleteFrame.clicked.connect(self.handleDeleteFrame)
        self.animationControlWidgetLayout.addWidget(self.deleteFrame)

        # File operations

        self.fileOperationsWidget = QWidget()
        self.fileOperationsWidget.setObjectName("fileOperations")
        self.fileOperationsWidgetLayout = QHBoxLayout(self.fileOperationsWidget)
        self.leftSideLayout.addWidget(self.fileOperationsWidget)
        self.leftSideLayout.setAlignment(self.fileOperationsWidget,Qt.AlignmentFlag.AlignBottom)

        self.frameNameEntry = QLineEdit()
        self.frameNameEntry.setMaximumWidth(350)
        self.frameNameEntry.setPlaceholderText("Image name")
        self.frameNameEntry.setText("Matrix animation")
        self.fileOperationsWidgetLayout.addWidget(self.frameNameEntry)

        self.saveButton = QPushButton(text="Save")
        self.saveButton.clicked.connect(self.handleSaveToFile)
        self.fileOperationsWidgetLayout.addWidget(self.saveButton)
        
        self.loadButton = QPushButton(text="Load from file")
        self.loadButton.clicked.connect(self.loadFromFile)
        self.fileOperationsWidgetLayout.addWidget(self.loadButton)

        # Device interaction

        self.actionsWidget = QWidget()
        self.actionLayout = QHBoxLayout(self.actionsWidget)
        self.leftSideLayout.addWidget(self.actionsWidget)

        self.playOnDevice = QPushButton(text="Play on device")
        self.playOnDevice.setCheckable(True)
        self.playOnDevice.setChecked(False)
        self.playOnDevice.clicked.connect(self.handlePlayOnDevice)
        self.actionLayout.addWidget(self.playOnDevice)

        self.sendButton = QPushButton(text="Send")
        self.sendButton.clicked.connect(self.sendToDevice)
        self.actionLayout.addWidget(self.sendButton)

        # Right side

        self.rightSide = QWidget()
        self.rightSideLayout = QVBoxLayout(self.rightSide)
        self.topWidgetLayout.addWidget(self.rightSide)

        self.preview = MatrixDisplay()
        self.preview.setMinimumWidth(500)
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
            FrameDisplayScroller{{
                background-color:{colors['bg-dark']};
                border: 1px solid {colors['border']};
                border-radius:10px;
            }}
            #deleteButton{{
                background-color:{colors['danger']}
            }}
            #fileOperations{{
                background-color: {colors['bg-light']};
                margin:0;
                padding:2px;
                border: 1px solid {colors['border']};
            }}
            QLineEdit{{
                border: 1px solid {colors['border']};
                background-color:{colors['bg-light']}
            }}
            #panelTitle{{
                font-size:24px;
            }}
        """)

    def handlePickerSelection(self):
        if self.pickerModeButton.isChecked():
            self.preview.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.preview.setCursor(Qt.CursorShape.ArrowCursor)

    def handleMatrixFill(self):
        self.animationObject["frames"][self.selectedFrameIndex] = [[self.selectedColorIndex for x in range(len(self.animationObject["frames"][self.selectedFrameIndex][0]))] for y in range(len(self.animationObject["frames"][self.selectedFrameIndex]))]
        self.loadFrameToPreview(self.selectedFrameIndex)

    def handlePreviewCallback(self,x,y):
        try:
            if self.pickerModeButton.isChecked():
                self.selectedColor = self.preview.pixelGrid[y][x]
                self.animationObject["palette"][self.selectedColorIndex] = self.selectedColor
                self.cards[self.selectedColorIndex].updateColor(self.selectedColor)
                self.colorDisplay.setStyleSheet(f"""
                    *{{background-color:rgba{self.selectedColor.getRgb()}}}
                """)
                self.pickerModeButton.setChecked(False)
                self.preview.setCursor(Qt.CursorShape.ArrowCursor)
                self.loadFrameToPreview(self.selectedFrameIndex)
            else:
                self.animationObject["frames"][self.selectedFrameIndex][y][x] = self.selectedColorIndex
                self.loadFrameToPreview(self.selectedFrameIndex)
        except Exception as e:
            showError(self,e)
    
    def handleOpenColorDialog(self):
        self.selectedColor=self.colorDialog.getColor(self.selectedColor)
        self.animationObject["palette"][self.selectedColorIndex] = self.selectedColor
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
        self.cards[self.selectedColorIndex].updateColor(self.selectedColor)
        self.loadFrameToPreview(self.selectedFrameIndex)

    def handlePaletteSelection(self):
        self.selectedColorIndex = int(self.colorRackButtonGroup.checkedButton().textData)-1
        self.selectedColor = self.animationObject["palette"][self.selectedColorIndex]
        self.colorDisplay.setStyleSheet(f"""
            *{{background-color:rgba{self.selectedColor.getRgb()}}}
        """)
    
    def loadFrameToPreview(self,index):
        try:
            frame = self.animationObject["frames"][index]
            QcolorFrame = [[self.animationObject["palette"][frame[b][a]] for a in range(len(frame[0]))] for b in range(len(frame))]
            self.preview.pixelGrid = QcolorFrame
            self.preview.update()
            self.animationCarousel.cards[index].setChecked(True)
            self.animationCarousel.updateDisplay(self.animationObject)
            self.frameLabel.setText(f"{self.selectedFrameIndex+1}/{len(self.animationObject["frames"])}")
        except Exception as e:
            showError(self,e)
    
    def resizeMatrix(self,w,h):
        try:
            self.preview.resizeMatrix(w,h)
            self.animationObject["frames"] = [[]]
            self.animationObject["frames"][0] = [[0 for x in range(w)] for y in range(h)]
            self.selectedFrameIndex = 0
            self.animationCarousel.updateDisplay(self.animationObject)
            self.loadFrameToPreview(0)
        except Exception as e:
            showError(self,e)

    def addBlank(self):
        try:
            if len(self.animationObject["frames"]) < 20:
                self.animationObject["frames"].append([[0 for a in range(len(self.animationObject["frames"][0][0]))] for b in range(len(self.animationObject["frames"][0]))])
                self.selectedFrameIndex = len(self.animationObject["frames"])-1
                self.loadFrameToPreview(self.selectedFrameIndex)
        except Exception as e:
            showError(self,e)

    def addDuplicate(self):
        try:
            if len(self.animationObject["frames"]) < 20:
                self.animationObject["frames"].append([[self.animationObject["frames"][self.selectedFrameIndex][b][a] for a in range(len(self.animationObject["frames"][0][0]))] for b in range(len(self.animationObject["frames"][0]))])
                self.selectedFrameIndex = len(self.animationObject["frames"])-1
                self.loadFrameToPreview(self.selectedFrameIndex)
        except Exception as e:
            showError(self,e)

    def handleFrameSelection(self):     
        self.selectedFrameIndex = self.animationCarousel.buttonGroup.checkedButton().number
        self.loadFrameToPreview(self.selectedFrameIndex)
    
    def handleDeleteFrame(self):
        try:
            if len(self.animationObject["frames"]) > 1:
                self.animationObject["frames"].pop(self.selectedFrameIndex)
                self.selectedFrameIndex = min(self.selectedFrameIndex,len(self.animationObject["frames"])-1)
                self.loadFrameToPreview(self.selectedFrameIndex)
        except Exception as e:
            showError(self,e)
    
    def playPause(self):
        try:
            if self.playButton.isChecked():
                self.selectedFrameIndex = 0
                self.playButton.setText("Stop")
                self.playTimer.start(self.speed)
            else:
                self.playButton.setText("Play")
                self.playTimer.stop()
                self.loadFrameToPreview(self.selectedFrameIndex)
        except Exception as e:
            showError(self,e)
        
    def nextFrame(self):
        self.loadFrameToPreview(self.selectedFrameIndex)
        self.selectedFrameIndex += 1
        if self.selectedFrameIndex >= len(self.animationObject["frames"]):
            self.selectedFrameIndex = 0
    
    def handlePlayOnDevice(self):
        self.controller.play()

    def sendToDevice(self):
        self.controller.sendAnimation(self.animationObject)

    def _coordinatesToAddress(self,x,y,originalDX):
        x+=1;y+=1
        address = originalDX*y
        if y%2==0: address -= x
        else: address-=originalDX-x+1
        return address

    def _oneDArrayToMatrix(self,oneD,originalDX,originalDY):
        matrix = [[0 for a in range(originalDX)] for b in range(originalDY)]
        for y in range(originalDY):
            for x in range(originalDX):
                matrix[y][x] = oneD[self._coordinatesToAddress(x,y,originalDX)]
        return matrix
    
    def loadFromFile(self):
        try:
            with open("config.json","r") as f: config = json.load(f)
            filenameDialog = QFileDialog(filter=".json")
            filename = filenameDialog.getOpenFileName(self,"Load matrix",config["savePath"])
            if not filename[0]: return
            if not os.path.exists(filename[0]): raise FileNotFoundError("File doesn't seem to exist!")
            with open(filename[0],"r") as f: data=json.load(f)
            if data.get("type") != "animation" and not data.get("ratingSum"): raise ValueError("Invalid json file, file doens't contain an animation!")
            self.frameNameEntry.setText(data.get("name","noname"))

            self.basicsPanel.speedSlider.setValue(min(1000,data.get("delay")))
            self.basicsPanel.speedSliderLetGo()

            # Load frames
            if data.get("frames"):
                deviceX = len(self.animationObject["frames"][0][0])
                deviceY = len(self.animationObject["frames"][0])
                originalX = data.get("gridWidth")
                originalY = data.get("gridHeight")
                self.animationObject["frames"] = [[[0 for a in range(deviceX)] for b in range(deviceY)] for i in range(len(data.get("frames")))]
                for i,frame in enumerate(data.get("frames")):
                    dataFrame = self._oneDArrayToMatrix(frame,originalX,originalY)
                    for y in range(min(deviceY,originalY)):
                        for x in range(min(deviceX,originalX)):
                            self.animationObject["frames"][i][y][x] = int(dataFrame[y][x])
                            print(int(dataFrame[y][x]))
            else:
                raise ValueError("No frames in animation json!")

            # Load palette
            if data.get("palette"):
                for i,color in enumerate(data.get("palette")):
                    self.animationObject["palette"][i] = QColor(color[0],color[1],color[2])
            else:
                self.animationObject["palette"] = [QColor("black"),QColor("red"),QColor("green"),QColor("blue"),QColor("yellow"),QColor("magenta"),QColor("cyan"),QColor("white"),QColor("#FF9911"),QColor("#00FF88")]
            
            self.selectedColorIndex = 0
            self.selectedFrameIndex = 0
            for i, color in enumerate(self.animationObject["palette"]):
                self.cards[i].updateColor(color)
            self.loadFrameToPreview(self.selectedFrameIndex)
        except Exception as e:
            showError(self,e)

    def handleSaveToFile(self):
        try:
            with open("config.json","r") as f: config = json.load(f)
            filenameDialog = QFileDialog(filter=".json")
            filename = filenameDialog.getSaveFileName(self,"Save matrix animation",os.path.join(config["savePath"],f"{self.frameNameEntry.text()}.json"))
            filename = filename[0]
            if not filename: raise ValueError("can't save to empty filename!")
            
            data = {
                "name":self.frameNameEntry.text(),
                "delay":self.speed,
                "type":"animation",
                "gridWidth":len(self.preview.pixelGrid[0]),
                "gridHeight":len(self.preview.pixelGrid),
                "palette": [(i.getRgb()[0],i.getRgb()[1],i.getRgb()[2]) for i in self.animationObject["palette"]],
                "frames": [self.controller._matrixToOneDimensionArray(i) for i in self.animationObject["frames"]]
            }

            with open(filename,"w") as f:
                json.dump(data,f,indent=4)
        except Exception as e:
            showError(self,e)