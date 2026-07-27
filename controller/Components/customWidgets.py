from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtCore import Qt
from colors import colors

class SegmentedButton(QWidget):
    def __init__(self,values,default_index=0):
        super().__init__()
        self.values = values
        self.layout = QHBoxLayout(self)
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