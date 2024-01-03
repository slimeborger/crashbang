import sys
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QVariantAnimation , QEasingCurve
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow
import backend

class FlashOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.move(0, 0)
        self.show()
        # TODO: Automatically adjust resolution
        self.setFixedSize(1920, 1080)
        self.setObjectName("overlay")
        
        # Read and apply stylesheet from file 'overlay.stylesheet' to [style_sheet]
        style_file = "overlay.stylesheet"
        with open(style_file, "r") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet)

        # Create an instance of the backend for calls
        self.backend_inst = backend.ScreenCapture()

        self.show_flash_border = False
        self.bg_transparent = True
        self.is_flashing = False    
        self.btn_screen_check()



    # def toggle_background(self):
    #     # Toggle the transparency of the background
    #     self.bg_transparent = not self.bg_transparent
    #     self.setStyleSheet(self.style_sheet if self.bg_transparent else "QMainWindow#overlay {background-color: rgba(0, 0, 0, 125)}")
    #     self.update()
        
    def flash_animation(self):
        # Initiate the flashing animation
        self.is_flashing = True
        self.border_flash(20, 100)
        QTimer.singleShot(20*100,self.fullscreen_flash)

    # A 'button' function (idk what it actually is). 
    # Calls other functions that require args.
    def btn_screen_check(self):
        print("START SCREEN CHECK")
        self.check_screen(100, 500)

    def border_flash(self, flash_count: int, flash_delay_ms: int):
        """
        Recursive function that flips [show_flash_border] to show/hide the flash rectangle. 
        Uses a QTimer that runs for [flash_delay_ms] milliseconds. 

        Arguments:
        * flash_count (int): Number of flips. Each flash is 2 flips so an even number is better.
        * flash_delay_ms (int): Delay in ms between flips
        """

        def recursive_callback():
            flash_delay_timer.stop()
            self.show_flash_border = not self.show_flash_border
            self.update()
            self.border_flash(flash_count - 1, flash_delay_ms)

        if flash_count <= 0:
            self.show_flash_border = False
            return

        flash_delay_timer = QTimer(self)
        flash_delay_timer.timeout.connect(recursive_callback)
        flash_delay_timer.start(flash_delay_ms)
        self.update()


    def check_screen(self, poll_count: int = 100, polling_time: int = 500):
        """
        Recursive function that calls [check_for_flash()] from backend to check if the screen needs to be flashed.
        Uses QTimers that run for [polling_time] milliseconds. Use [poll_count] to limit the number of checks.
         
        Arguments:
        * poll_count (int): Number of times check_screen() is recursively called before it fully terminates.
        * polling_time (int): Delay in ms between checks
        """
        def backend_callback():
            poll_timer.stop()
            check_result = self.backend_inst.check_for_flash(polling_time)
            if check_result == True and self.is_flashing == False:
                self.flash_animation()
            self.check_screen(poll_count - 1)

        if poll_count <= 0:
            print("Finished backend callback")
            return
        poll_timer = QTimer(self)
        poll_timer.timeout.connect(backend_callback)
        poll_timer.start(polling_time)

    def fullscreen_flash(self):

        def flash_cooldown():
            print("Start cooldown")
            self.setStyleSheet(
                    "QMainWindow#overlay {background-color: rgba(255, 255, 255, 0 ) }"
            )
            # self.bg_transparent = True
            self.is_flashing = False;
            # self.backend_inst.close_app()
            # self.backend_inst.lock_screen()
        
        def flash_fade_out():
            fading_alpha_anim = QVariantAnimation(self)
            fading_alpha_anim.setDuration(3500)
            fading_alpha_anim.setStartValue(255)
            fading_alpha_anim.setEndValue(0)


            fading_alpha_anim.valueChanged.connect(
                lambda: update_alpha(fading_alpha_anim)
                )
            
            fading_alpha_anim.start()
            fading_alpha_anim.finished.connect(flash_cooldown)

            
        def update_alpha(anim:QVariantAnimation):
            alpha_val =int(anim.currentValue())
            self.setStyleSheet(
                    f"QMainWindow#overlay {{background-color: rgba(255, 255, 255, {alpha_val} ) }}"
            )

        self.bg_transparent = False
        QTimer.singleShot(500,flash_fade_out)
        # QTimer.singleShot(10000,flash_cooldown)

    def paintEvent(self, event):
        p = QPainter(self)
        self.flash_rect = [0, 0, 1920, 1080]
        p.setPen(QPen(Qt.GlobalColor.white, 30))
        brush = QBrush(QColor(0, 0, 0, 0), Qt.BrushStyle.SolidPattern)
        p.setBrush(brush)
        if self.show_flash_border:
            p.drawRect(*self.flash_rect)

