import sys
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QVariantAnimation , QEasingCurve
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,QGridLayout
import PyQt6.QtWidgets
import backend, overlay

class SettingsGUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(640, 360)
        self.setObjectName("settings")
        layout = QGridLayout()
        
        
        # Read and apply stylesheet from file to [style_sheet]
        """     
        style_file = "settings.stylesheet"
        with open(style_file, "r") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet) """

        # Create an instance of the backend for calls
        self.backend_inst = backend.ScreenCapture()

        # GUI Widgets: Flash, Exit
        toggle_btn = PyQt6.QtWidgets.QPushButton("Start Crashbang",self)
        layout.addWidget(toggle_btn,0,0)
        toggle_btn.clicked.connect(overlay.FlashOverlay)

        lock_on_flash_checkbox = PyQt6.QtWidgets.QCheckBox("Lock Screen")
        lock_on_flash_checkbox.stateChanged.connect(
            lambda: self.backend_inst.options_set("lock_screen",lock_on_flash_checkbox.isChecked())
        )
        layout.addWidget(lock_on_flash_checkbox,1,0)

        exit_btn = PyQt6.QtWidgets.QPushButton("Exit",self)
        exit_btn.clicked.connect(sys.exit)    
        layout.addWidget(exit_btn,0,1)

        self.setLayout(layout)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    main = SettingsGUI()
    # main.move(100, 100)
    main.show()
    try:
        sys.exit(application.exec())
    except Exception:
        print("Error")