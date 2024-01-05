from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QVariantAnimation , QEasingCurve
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget
import backend
from settings import Settings

class Flash(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.move(0, 0)

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

        self.fullscreen_flash_alpha = 0
        self.border_flash_alpha = 0

        self.show_flash_border = False
        self.is_flashing = False    

        self.check_screen(100, 500)
        self.show()
        print(f"Overlay Call: {Settings.get('lock_screen')}")


        
    def flash_animation(self):
        # Initiate the flashing animation
        self.is_flashing = True
        self.border_flash(5, 500)
        QTimer.singleShot(500*5,lambda: self.border_flash(10,200))
        QTimer.singleShot(200*10 + 500*6,self.fullscreen_flash)

        

    def border_flash(self, flash_limit: int, flash_delay_ms: int):
        """
        Recursive function that flips [show_flash_border] to show/hide the flash rectangle. 
        Uses a QTimer that runs for [flash_delay_ms] milliseconds. 

        Arguments:
        * flash_count (int): Number of flips. Each flash is 2 flips so an even number is better.
        * flash_delay_ms (int): Delay in ms between flips
        """
        border_flash_anim = QVariantAnimation(self)
        border_flash_anim.setDuration(flash_delay_ms)
        border_flash_anim.setStartValue(0)
        border_flash_anim.setEndValue(0)
        border_flash_anim.setKeyValueAt(0.5,255)
        border_flash_anim.setLoopCount(flash_limit)

        border_flash_anim.start()
        border_flash_anim.valueChanged.connect(
            lambda: update_alpha(border_flash_anim)
        )

        def update_alpha(anim:QVariantAnimation):
            self.border_flash_alpha = int(anim.currentValue())
            self.update()
        

    def check_screen(self, poll_limit: int = 100, polling_time: int = 500):
        """
        Recursive function that calls [check_for_flash()] from backend to check if the screen needs to be flashed.
        Uses QTimers that run for [polling_time] milliseconds. Use [poll_limit] to limit the number of checks.
         
        Arguments:
        * poll_limit (int): Number of times check_screen() is recursively called before it fully terminates.
        * polling_time (int): Delay in ms between checks
        """
        poll_count = 0

        def backend_call():
            nonlocal poll_count
            poll_count += 1
            if poll_count >= poll_limit:
                poll_timer.stop()
                print("Finished backend callback")
            else:
                check_result = self.backend_inst.check_for_flash(polling_time)
                if check_result == True and self.is_flashing == False:
                    self.flash_animation()

        poll_timer = QTimer(self)
        poll_timer.timeout.connect(backend_call)
        poll_timer.start(polling_time)

    def fullscreen_flash(self):

        def flash_cooldown():
            self.is_flashing = False
            print(Settings.get("lock_screen"))
            self.backend_inst.lock_screen(Settings.get("lock_screen"))
         
        def update_alpha(anim:QVariantAnimation):
            self.fullscreen_flash_alpha = int(anim.currentValue())
            self.update()

        fading_alpha_anim = QVariantAnimation(self)
        fading_alpha_anim.setDuration(3500)
        fading_alpha_anim.setStartValue(255)
        fading_alpha_anim.setEndValue(0)

        fading_alpha_anim.valueChanged.connect(
            lambda: update_alpha(fading_alpha_anim)
            )
        
        fading_alpha_anim.start() 
        fading_alpha_anim.finished.connect(flash_cooldown)


    def paintEvent(self, event):
        p = QPainter(self)
        self.flash_rect = [0, 0, 1920, 1080]
        p.setPen(QPen(QColor(0,0,0,self.border_flash_alpha), 30))
        brush = QBrush(QColor(0, 0, 0, 0), Qt.BrushStyle.SolidPattern)
        p.setBrush(brush)
        p.drawRect(*self.flash_rect)
        p.fillRect(event.rect(), QColor(0, 0, 0, self.fullscreen_flash_alpha))

