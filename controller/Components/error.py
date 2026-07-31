from PyQt6.QtWidgets import QMessageBox
from colors import colors
from PyQt6.QtGui import QFontDatabase, QFont

def showError(parent,message):
    dialog = QMessageBox(parent)
    dialog.setIcon(QMessageBox.Icon.Critical)
    dialog.setWindowTitle("Error")
    dialog.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
    dialog.setStyleSheet(f"""
        *{{
            font-size:16px;
            font-family:'Pixelify Sans';
            color:{colors['text']};
            border-radius: 5px;
            padding:5px;
            height:20px;
            background-color:{colors['bg-light']}
        }}
        QPushButton{{
            border: 1px solid {colors['border']};
            background-color:{colors['bg-light']};
            padding:4px 20px;
        }}
        QPushButton:pressed{{
            border-color:{colors['highlight']}
        }}
        QPushButton:hover{{
            background-color:{colors['border-muted']};
        }}

        QCheckBox{{
            background-color:{colors['bg']};
            border: 1px solid {colors['border']};
        }}
        QCheckBox:checked{{
            background-color:{colors['highlight']};
            border: 1px solid {colors['border']};
        }}
    """)
    dialog.setText(str(message))
    dialog.exec()