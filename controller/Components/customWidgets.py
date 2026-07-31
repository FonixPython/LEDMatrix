from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout,QVBoxLayout, QPushButton, QButtonGroup, QScrollArea
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush
from colors import colors
from Components.error import showError
class SegmentedButton(QWidget):
    def __init__(self,values,orientation="horizontal",default_index=0):
        super().__init__()
        self.values = values
        self.layout = QHBoxLayout(self) if orientation == "horizontal" else QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(2,2,2,2)


        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)

        for i, value in enumerate(values):
            button = QPushButton(text=value)
            button.setCheckable(True)
            button.setFixedHeight(38)
            button.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            if i == default_index:button.setChecked(True)
            self.buttonGroup.addButton(button)
            self.layout.addWidget(button,1)

    def getValue(self):
        return self.buttonGroup.checkedButton().text()

class MatrixDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.x = 8
        self.y = 8
        self.pixelGrid = [[QColor("black") for a in range(self.x)] for b in range(self.y)]
        self.callback = None
        self.painting = False
        self.lastX = None
        self.lastY = None
    
    def resizeMatrix(self,x,y):
        try:
            self.x = x
            self.y = y
            self.pixelGrid = [[QColor("black") for a in range(self.x)] for b in range(self.y)]
            self.update()
        except Exception as e:
            showError(self,e)
    
    def paintEvent(self,event):
        padding = 5
        painter = QPainter(self)
        
        cellSize = min(
            (self.width()-(padding*self.x)) / self.x,
            (self.height()-(padding*self.y)) / self.y
        )
        
        painter.setPen(Qt.PenStyle.NoPen)
        for y in range(self.y):
            for x in range(self.x):
                rect = QRectF(
                    x * (cellSize + padding),
                    y * (cellSize + padding),
                    cellSize,
                    cellSize
                )
                painter.setBrush(QBrush(self.pixelGrid[y][x]))
                painter.fillRect(rect, QColor(colors['bg-light']))
                painter.drawRoundedRect(rect,15,15)
    
    def mousePressEvent(self, event):
        self.painting = True
        padding = 5
        cellSize = min(
            (self.width()-(padding*self.x)) / self.x,
            (self.height()-(padding*self.y)) / self.y
        )

        step = cellSize + padding

        mx = event.position().x()
        my = event.position().y()

        x = int(mx / step)
        y = int(my / step)
        
        if 0 <= x < self.x and 0 <= y < self.y:
            self.lastX = x
            self.lastY = y
            self.callback(x,y)

    def mouseMoveEvent(self,event):
        if self.painting:
            padding = 5
            cellSize = min(
                (self.width()-(padding*self.x)) / self.x,
                (self.height()-(padding*self.y)) / self.y
            )

            step = cellSize + padding

            mx = event.position().x()
            my = event.position().y()

            x = int(mx / step)
            y = int(my / step)
            
            if self.lastX != x or self.lastY != y:
                if 0 <= x < self.x and 0 <= y < self.y:
                    self.lastX = x
                    self.lastY = y
                    self.callback(x,y)

    def mouseReleaseEvent(self,event):
        self.painting = False

class ColorCard(QPushButton):
    def __init__(self,text,color):
        super().__init__()
        self.color = color
        self.textData = text
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(QLabel(text))
        
        self.preview = QWidget()
        self.preview.setFixedSize(250,40)
        self.preview.setStyleSheet(f"""
            background: rgba{self.color.getRgb()};
            border-radius: 10px;
        """)
        self.layout.addWidget(self.preview)

        self.toggled.connect(self.updateStyle)
        self.updateStyle(False)

    def updateStyle(self, checked):
        if checked:self.setProperty("selected", True)
        else:self.setProperty("selected", False)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def updateColor(self,color):
        self.color = color
        self.preview.setStyleSheet(f"""
            background: rgba{self.color.getRgb()};
            border-radius: 10px;
        """)

class TinyMatrix(QWidget):
    def __init__(self,frame):
        super().__init__()
        self.frame = frame

    def paintEvent(self,event):
        painter = QPainter(self)
        cellSize = min(
            90 / len(self.frame[0]),
            90 / len(self.frame)
        )
        self.setFixedSize(int(cellSize*len(self.frame[0])),int(cellSize*len(self.frame)))
        for y in range(len(self.frame)):
            for x in range(len(self.frame[0])):
                rect = QRectF(
                    x * cellSize,
                    y * cellSize,
                    cellSize,
                    cellSize
                )
                painter.fillRect(rect,self.frame[y][x])

class TinyDisplayCard(QPushButton):
    def __init__(self,frame,number):
        super().__init__()
        self.number = number
        self.setCheckable(True)
        self.setChecked(False)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5,5,5,5)
        self.matrix = TinyMatrix(frame)
        self.matrix.setFixedSize(90,90)
        self.setFixedSize(100,100)
        self.layout.addWidget(self.matrix)
        self.layout.setAlignment(self.matrix,Qt.AlignmentFlag.AlignCenter)


    def updateFrame(self,frame):
        self.matrix.frame = frame
        self.matrix.update()

class FrameDisplayScroller(QScrollArea):
    def __init__(self,animationObject,maxFrames):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.maxFrames = maxFrames
        self.scrolledWidget = QWidget()
        self.scrolledWidget.setObjectName("scrolledWidget")
        self.scrolledWidget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.scrolledWidgetLayout = QHBoxLayout(self.scrolledWidget)
        self.setWidget(self.scrolledWidget)
        self.setWidgetResizable(False)
        self.cards = []
        self.buttonGroup = QButtonGroup(self.scrolledWidget)
        self.buttonGroup.setExclusive(True)
        for i in range(maxFrames):
            frame = [[QColor("black") for i in range(8)] for x in range(8)]
            card = TinyDisplayCard(frame,i)
            card.setVisible(False)
            self.buttonGroup.addButton(card)
            if i == 0: card.setChecked(True)
            self.scrolledWidgetLayout.addWidget(card)
            self.cards.append(card)
        self.scrolledWidget.adjustSize()
        self.scrolledWidgetLayout.addStretch()
        self.updateDisplay(animationObject)
        
    def updateDisplay(self,animationObject):
        for i,frame in enumerate(animationObject["frames"]):
            self.cards[i].updateFrame(frame=[[animationObject["palette"][frame[b][a]] for a in range(len(frame[0]))] for b in range(len(frame))])
            self.cards[i].setVisible(True)
        for i in range(len(animationObject["frames"]),self.maxFrames):
            self.cards[i].setVisible(False)
        self.scrolledWidget.adjustSize()
