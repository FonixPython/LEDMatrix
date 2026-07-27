from PyQt6.QtWidgets import QLabel,QWidget, QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from colors import colors


class BasicsPanel(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.layout = QVBoxLayout()