import sys
import backend
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

        #Create an instance of the backend for calls
        self.backend_inst = backend.ScreenCapture()

        self.show_flash_border = False
        self.bg_transparent = True
        self.is_flashing = False

        #GUI Widgets: Flash, Exit

        self.toggle_btn = QPushButton("Toggle", self)
        self.toggle_btn.setGeometry(200, 150, 100, 30)
        self.toggle_btn.clicked.connect(self.toggle_background)
        self.draw_btn = QPushButton("Start Code", self)
        self.draw_btn.setGeometry(320, 150, 100, 30)
        self.draw_btn.clicked.connect(self.btn_screen_check)

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


    def flash_animation(self):
        self.is_flashing = True
        self.border_flash(20,100)


    #A 'button' function (idk what it actually is). 
    #calls other functions that require args.
    def btn_screen_check(self):
        self.check_screen(100,500)


    def border_flash(self,flash_count: int,flash_delay_ms: int):
        """
        Recursive function that flips [show_flash_border] to show/hide the flash rectangle. 
        Uses a QTimer that runs for [flash_delay_ms] milliseconds. 

        Arguments:
        * flash_count (int): Number of flips. Each flash is 2 flips so an even number is better.
        * flash_delay_ms (int): Delay in ms between flips
        """

        def recursive_callback():
            flash_delay_timer.stop()
            self.border_flash(flash_count - 1, flash_delay_ms)

        if flash_count <= 0:
            self.show_flash_border = False
            self.is_flashing = False
            self.update()
            return None

        flash_delay_timer = QTimer(self)
        flash_delay_timer.timeout.connect(recursive_callback)
        flash_delay_timer.start(flash_delay_ms)
        self.show_flash_border = not self.show_flash_border
        self.update()
        return None

    def check_screen(self,poll_count: int = 100, polling_time: int = 500):
        """
        Recursive function that calls [check_for_flash()] from backend to check if screen needs to be flashed.
        Uses QTimers that runs for [polling_time] milliseconds. Use [poll_count] to limit number of checks.
         
        Arguments:
        * poll_count (int): Number of times check_screen() is recursively called before it fully terminates.
        * polling_time (int): Delay in ms between checks

        """
        def backend_callback():
            poll_timer.stop()
            check_result = self.backend_inst.check_for_flash(polling_time)
            print(check_result)
            if check_result == True and self.is_flashing == False:
                self.flash_animation()
            self.check_screen(poll_count - 1)

        if poll_count <= 0:
            print("Finished backend callback")
            return None
        poll_timer = QTimer(self)
        poll_timer.timeout.connect(backend_callback)
        poll_timer.start(polling_time)
        return None



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