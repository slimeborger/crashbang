import sys,os,ctypes,time, subprocess

class ScreenCapture():
    
    target_window = ""

    def __init__(self):
        self.start_time = time.time()
        self.blacklist_windows = set(
            [
            "Program Manager",
            "Windows Input Experience"
            ]
        )
        self.target_window_duration = 0
        self.target_window_limit = 4000

    @classmethod
    def set_target_window(cls, window_title:str):
        cls.target_window = window_title
        print(f"Set target_window to {cls.target_window}")
        
    @classmethod
    def get_target_window(cls):
        return cls.target_window
    


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
        target_window = ScreenCapture.get_target_window()
        old_window_title = ""
        window_title = self.get_focused_window()[1]       
        #Detect window change
        if old_window_title != window_title:
            if (old_window_title == target_window):
                elapsed_time = time.time() - self.start_time
                self.start_time = time.time()
            old_window_title = window_title
        #Measure how long user focuses on [target_window]
        if window_title == target_window:
            self.target_window_duration += polling_time_ms
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
                
        return [window_handle, str(buffer.value)]
    
    def get_running_applications(self):
        def filter_and_add_window(hwnd, lParam):
            titles = lParam[0]
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                buffer_length = 256
                buffer = ctypes.create_unicode_buffer(buffer_length)
                ctypes.windll.user32.GetWindowTextW(hwnd, buffer, buffer_length)
                if not (buffer.value == '' or buffer.value in self.blacklist_windows):
                    titles.append(buffer.value)
            return True

        titles = []
        ctypes.windll.user32.EnumWindows(
            ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_ulong, ctypes.POINTER(ctypes.py_object))(filter_and_add_window),
            ctypes.byref(ctypes.py_object(titles))
        )
        return titles
    
    def lock_screen(self,isTrue:bool):
        """Lock the user's workstation if the option is True"""
        if isTrue:
            ctypes.windll.user32.LockWorkStation()

    def close_app(self,isTrue:bool,window_handle):
        if isTrue:
            ctypes.windll.user32.PostMessageW(window_handle, 0x0010, 0, 0)
            
    def exit(self):
        sys.exit()


if __name__ == "__main__":
    ScreenCapture()