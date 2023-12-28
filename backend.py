import sys,os,ctypes,time
import numpy as np

class ScreenCapture():
    def __init__(self):
        self.start_flash = False
        self.start_time = time.time()
        self.target_window_duration = 0


    def check_for_flash(self,polling_time_ms:int) -> bool:
        """
        Check if the user needs to be flashed by using [get_focused_window()] to see if
        the user is focusing on a [target_window] for more than [] seconds. Returns the bool 
        [start_flash] which can be used to do GUI processes.

        Arguments:
        * polling_time (int): Time in ms to be added.

        """
        old_window_title = ""
        target_window = "Settings"#str(input("Target Window: ")
        window_title = self.get_focused_window()       
        #Detect window change
        if old_window_title != window_title:
            if (old_window_title == target_window):
                elapsed_time = time.time() - self.start_time
                self.start_time = time.time()
            old_window_title = window_title
        #Measure how long user focuses on [target_window]
        if window_title == target_window:
            self.target_window_duration += polling_time_ms

        if self.target_window_duration >= 5000:
            print("SCREEN FLASH")
            self.start_flash = True
            self.target_window_duration = 0
        else:
            self.start_flash = False

        print(f"Focused on {window_title}")

        return self.start_flash
        
                
    def get_focused_window(self) -> str:
        """
        Returns the title of the window the user is currently focused on, as a string.

        Returns: 
        * window_title (str): The title of the window.
        """    

        # Get the handle of the foreground window and get window title string length via ctypes
        #I'll be honest I have no idea what the underlying process is but if it works it works.
        window_handle = ctypes.windll.user32.GetForegroundWindow()
        window_title_len = ctypes.windll.user32.GetWindowTextLengthW(window_handle) + 1
        
        #Create a C array of unicode characters (buffer) and write title to it.
        buffer = ctypes.create_unicode_buffer(window_title_len)
        ctypes.windll.user32.GetWindowTextW(window_handle, buffer, window_title_len)
        
        return str(buffer.value)



if __name__ == "__main__":
    ScreenCapture()
