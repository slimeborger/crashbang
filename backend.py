import sys,os,ctypes,time, subprocess

class ScreenCapture():
    def __init__(self):
        #[start_flash] determines whether or not
        self.start_flash = False
        self.start_time = time.time()
        self.target_window_duration = 0
        self.target_window_limit = 4000

        self.options = {
            "lock_screen": True,
            "close_active_window": True
        }

    def options_set(self,option, value):
        try: 
            self.options[option] = value
            print(f"Set {option} to {value}")
        except KeyError:
            return 

    def check_for_flash(self,polling_time_ms:int) -> bool:
        """
        Check if the user needs to be flashed by using [get_focused_window()] to see if
        the user is focusing on a [target_window] for more than [] seconds. 
        Returns a bool which can be used for flashing checks

        Arguments:
        * polling_time (int): Time in ms to be added.

        Returns:
        * bool

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
        # print(window_title)
        if self.target_window_duration >= self.target_window_limit:
            self.target_window_duration = 0
            return True
        else:
            return False
        
                
    def get_focused_window(self) -> str:
        """
        Return the title of the window the user is currently focused on, as a string.

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
    
    def lock_screen(self):
        ctypes.windll.user32.LockWorkStation()

    def close_app(self,window):
        subprocess.call(["taskkill","/F","/IM","firefox.exe"])



if __name__ == "__main__":
    ScreenCapture()
