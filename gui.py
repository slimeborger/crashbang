import sys
import screen_capture
from PyQt6.QtCore import Qt, QFile, QTimer ,pyqtBoundSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget
import numpy as np
import time

class FlashOverlay(QMainWindow):



    def __init__(self):
        super().__init__()

        #TODO: Automatically adjust resolution
        self.setFixedHeight(1080)
        self.setFixedWidth(1920)
        self.setObjectName("overlay")
        
        #Read and apply stylesheet from file 'overlay.stylesheet' to [style_sheet]
        style_file = "overlay.stylesheet"
        with open(style_file,"r") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet)



        self.bg_transparent = True
        self.show_flash_border = False

        #GUI Widgets: Flash, Exit

        self.toggle_btn = QPushButton("Toggle", self)
        self.toggle_btn.setGeometry(200, 150, 100, 30)
        self.toggle_btn.clicked.connect(self.toggle_background)
        self.draw_btn = QPushButton("Start Code", self)
        self.draw_btn.setGeometry(320, 150, 100, 30)
        self.draw_btn.clicked.connect(self.check_screen)

        self.close_btn = QPushButton("Exit", self)
        self.close_btn.setGeometry(200, 200, 100, 30)
        self.close_btn.clicked.connect(sys.exit)


        

    def toggle_background(self):
        self.bg_transparent =  not  self.bg_transparent
        if self.bg_transparent:
            self.setStyleSheet(self.style_sheet)
        else:
            self.setStyleSheet("QMainWindow#overlay {background-color: rgba(0, 0, 0, 125)}")
        self.update()


    # Called when button pressed, can be customised to change flash animation.
    def flash_sequence(self):
        self.border_flash(20,1000)


    def border_flash(self,flash_count: int,flash_delay_ms: int):
        """
        Recursively function that flips [show_flash_border] to show/hide the flash rectangle. 
        Uses a QTimer that runs for [flash_delay_ms] milliseconds. Use [flash_count] to count number of flips.

        Arguments:
        * flash_count (int): Number of flips. Each flash is 2 flips so an even number is better.
        * flash_delay_ms (int): Delay in ms between flips
        """

        def recursive_callback():
            delay_timer.stop()
            self.border_flash(flash_count - 1, flash_delay_ms)
        if flash_count <= 0:
            self.show_flash_border = False
            self.update()
            return None
        delay_timer = QTimer(self)
        delay_timer.timeout.connect(recursive_callback)
        delay_timer.start(flash_delay_ms)
        self.show_flash_border = not self.show_flash_border
        self.update()

    def check_screen(self):
            def backend_callback():
                polling_timer.stop()
                instance = screen_capture.main()
                check_result = instance.check_for_flash(4000)
                if check_result == True:
                    self.flash_sequence()

            polling_timer = QTimer(self)
            polling_timer.start(4000)
            polling_timer.timeout.connect(backend_callback)





    def paintEvent(self, event):
        p = QPainter(self)
        self.flash_rect = [0,0,1920,1080]
        p.setPen(QPen(Qt.GlobalColor.red, 30))
        p.setBrush(QBrush(QColor(0, 0, 0, 0), Qt.BrushStyle.SolidPattern))
        if self.show_flash_border == True:
            p.drawRect(*self.flash_rect)
        


if __name__ == "__main__":
    application = QApplication(sys.argv)
    main = QStackedWidget()
    main.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    main.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    main.move(0, 0)
    overlay = FlashOverlay()
    main.addWidget(overlay)
    main.show()

    try:
        sys.exit(application.exec())
    except Exception:
        print("Error")