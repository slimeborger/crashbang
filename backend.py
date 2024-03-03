import sys,os,ctypes,time, subprocess
from settings import Settings

class ScreenCapture():
    
    """
    Class for observing user's active windows and how long they have spent focused on target window(s).
    
    Class Methods:
    * :func: `set_target_window`
    * :func: `get_target_window`
    
    """

    target_window = ""

    def __init__(self):
        self.start_time = time.time()
        self.blacklist_windows = set(
            [
            "Program Manager",
            "Windows Input Experience",
            "Crashbang - Settings"
            ]
        )
        self.target_window_duration = 0
        
    @classmethod
    def set_target_window(cls, window_title:str):
        cls.target_window = window_title
        print(f"Set target_window to {cls.target_window}")
        
    @classmethod
    def get_target_window(cls):
        return cls.target_window
    


    def check_for_flash(self,polling_time_ms:int,target_window_limit:int) -> bool:
        """
        Check if the user needs to be flashed by using [get_focused_window()] to see if the user is focusing on a [target_window] for more than [target_window_limit] ms. 
        
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
        print(f"Elapsed: {self.target_window_duration}")
        print(f"Limit: {target_window_limit}")
        if window_title == target_window:
            self.target_window_duration += polling_time_ms
        if self.target_window_duration >= target_window_limit:
            self.target_window_duration = 0
            return True
        else:
            return False
        
                
    def get_focused_window(self) -> list[str]:
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
    
class PostFlashActions():
    
    def __init__(self) -> None:
        
        def exit_window(window_handle: str):
            ctypes.windll.user32.PostMessageW(window_handle, 0x0010, 0, 0)
            
        def lock_screen():
            ctypes.windll.user32.LockWorkStation()
            
        if Settings.get("lock_screen") == True:
            lock_screen()
        if Settings.get("close_active_window") == True:
            scr_capture = ScreenCapture()
            exit_window(scr_capture.get_focused_window()[0])

        
def exit():
    sys.exit()


if __name__ == "__main__":
    ScreenCapture()