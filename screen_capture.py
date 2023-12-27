import sys,os,ctypes,time
import numpy as np

class main():

    def __init__(self):
        super().__init__()
        self.start_flash = False
        target_window = "Settings"#str(input("Target Window: ")
        print("TEST")
        old_window_title = ""
        polling_time = 1 
        start_time = time.time()
        elapsed_time = 0
        target_window_duration = 0
        
        for i in range(50):
            window_title = self.get_focused_window()       

            #Detect window change
            if old_window_title != window_title:
                if (old_window_title == target_window):
                    elapsed_time = time.time() - start_time
                    start_time = time.time()
                old_window_title = window_title

            #Measure how long user focuses on [target_window]
            if window_title == target_window:
                target_window_duration += polling_time

            if target_window_duration >= 3:
                print("SCREEN FLASH")
                self.start_flash = True
                target_window_duration = 0
            
            print(f"Focused on {window_title}")

            #Check every [polling_time] seconds
            time.sleep(polling_time)
                
    def get_focused_window(self) -> str:
        """
        Returns the title of the window the user is currently focused on, as a string.

        Returns: 
        * window_title: str
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
    main()
