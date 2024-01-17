import sys
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QVariantAnimation , QEasingCurve
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,QGridLayout
import PyQt6.QtWidgets
import overlay, settings, backend

class SettingsGUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Crashbang - Settings")
        self.setFixedSize(640, 360)
        self.setObjectName("settings")
        layout = QGridLayout()        
        
        # Read and apply stylesheet from file to [style_sheet]
        """     
        style_file = "settings.stylesheet"
        with open(style_file, "r") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet) """

        # GUI Widgets: Flash, Exit
        toggle_btn = PyQt6.QtWidgets.QPushButton("Start Crashbang",self)
        layout.addWidget(toggle_btn,0,0)
        toggle_btn.clicked.connect(overlay.Flash)

        lock_screen_chkbox = PyQt6.QtWidgets.QCheckBox("Lock Screen",self)
        lock_screen_chkbox.stateChanged.connect(
            lambda: settings.Settings.set("lock_screen",lock_screen_chkbox.isChecked())
        )
        layout.addWidget(lock_screen_chkbox,1,0)

        
        close_app_chkbox = PyQt6.QtWidgets.QCheckBox("Close App",self)
        close_app_chkbox.stateChanged.connect(
            lambda: settings.Settings.set("close_active_window",close_app_chkbox.isChecked())
        )
        layout.addWidget(close_app_chkbox,2,0)

        exit_btn = PyQt6.QtWidgets.QPushButton("Exit",self)
        exit_btn.clicked.connect(sys.exit)    
        layout.addWidget(exit_btn,0,1)

        backend_inst = backend.ScreenCapture()

        def add_windows_to_dropdown():
            running_windows_dropdown.clear()
            windowArray = backend_inst.get_running_applications()
            running_windows_dropdown.addItems(windowArray)

        refresh_windows_btn = PyQt6.QtWidgets.QPushButton("RLD")
        refresh_windows_btn.clicked.connect(add_windows_to_dropdown)    
        layout.addWidget(refresh_windows_btn,1,2)

        running_windows_dropdown = PyQt6.QtWidgets.QComboBox(self)
        running_windows_dropdown.currentIndexChanged.connect(
            lambda: backend_inst.set_target_window(running_windows_dropdown.currentText())
            )
        layout.addWidget(running_windows_dropdown,0,3)
        
        self.setLayout(layout)
        add_windows_to_dropdown()

if __name__ == "__main__":
    application = QApplication(sys.argv)
    main = SettingsGUI()
    # main.move(100, 100)
    main.show()
    try:
        sys.exit(application.exec())
    except Exception:
        print("Error")