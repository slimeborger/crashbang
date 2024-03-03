import sys
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QVariantAnimation , QEasingCurve
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,QGridLayout
import PyQt6.QtWidgets as widget
import overlay, settings, backend

class SettingsGUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Crashbang - Settings")
        self.setFixedSize(640, 360)
        self.setObjectName("settings")
        layout = QGridLayout()
        
        backend_inst = backend.ScreenCapture()        
        # Read and apply stylesheet from file to [style_sheet]
        """     
        style_file = "settings.stylesheet"
        with open(style_file, "r") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet) """


        toggle_btn = widget.QPushButton("Start Crashbang",self)
        layout.addWidget(toggle_btn,0,0)
        toggle_btn.clicked.connect(overlay.Flash)

        lock_screen_chkbox = widget.QCheckBox("Lock Screen",self)
        lock_screen_chkbox.stateChanged.connect(
            lambda: settings.Settings.set("lock_screen",lock_screen_chkbox.isChecked())
        )
        layout.addWidget(lock_screen_chkbox,2,2)
        
        close_app_chkbox = widget.QCheckBox("Close App",self)
        close_app_chkbox.stateChanged.connect(
            lambda: settings.Settings.set("close_active_window",close_app_chkbox.isChecked())
        )
        layout.addWidget(close_app_chkbox,2,0)

        exit_btn = widget.QPushButton("Exit",self)
        exit_btn.clicked.connect(sys.exit)    
        layout.addWidget(exit_btn,0,1)
        
        delay_lbl = widget.QLabel(self)
        delay = settings.Settings.get("target_window_limit_ms")
        delay_lbl.setText(f"Current Delay: {delay}ms")
        layout.addWidget(delay_lbl,3,1)
        
        delay_slider = widget.QSlider(Qt.Orientation.Horizontal,self)
        delay_slider.setTickInterval(1)
        delay_slider.setTickPosition(widget.QSlider.TickPosition.TicksAbove)
        delay_slider.setRange(1,10)
        delay_slider.setValue(delay//1000)
        
        delay_slider.valueChanged.connect(
            lambda: update_delay(delay_slider.value()*1000)
        )
        
        layout.addWidget(delay_slider,3,0)
        
        running_windows_dropdown = widget.QComboBox(self)
        running_windows_dropdown.currentIndexChanged.connect(
            lambda: backend_inst.set_target_window(running_windows_dropdown.currentText())
            )
        layout.addWidget(running_windows_dropdown,1,0)
        
        def add_windows_to_dropdown():
            running_windows_dropdown.clear()
            windowArray = backend_inst.get_running_applications()
            running_windows_dropdown.addItems(windowArray)
        
        def update_delay(value: int):
            settings.Settings.set("target_window_limit_ms",value)
            delay = settings.Settings.get("target_window_limit_ms")
            delay_lbl.setText(f"Current Delay: {delay}ms")
            
        refresh_windows_btn = widget.QPushButton("RLD")
        refresh_windows_btn.clicked.connect(add_windows_to_dropdown)    
        layout.addWidget(refresh_windows_btn,1,4)
        
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