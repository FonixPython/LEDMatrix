from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout,QVBoxLayout,QAbstractButton, QPushButton, QButtonGroup
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush
from colors import colors


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
        self.x = x
        self.y = y
        self.pixelGrid = [[QColor("black") for a in range(self.x)] for b in range(self.y)]
        self.update()
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
            
            
            print(x,y)
            if self.lastX != x or self.lastY != y:
                print(x,y)
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
        self.setFixedHeight(60)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(QLabel(text))
        
        self.preview = QWidget()
        self.preview.setFixedSize(350,60)
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


