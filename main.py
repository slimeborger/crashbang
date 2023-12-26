import sys
import os
import ctypes
import time

def main():

    target_window = "Settings"#str(input("Target Window: ")
    old_window_title = ""
    start_time = time.time()
    elapsed_time = 0
    target_window_duration = 0
    


    for i in range(50):

        # Get the handle of the foreground window and get window title string length
        window_handle = ctypes.windll.user32.GetForegroundWindow()
        window_title_len = ctypes.windll.user32.GetWindowTextLengthW(window_handle) + 1
        
        buffer = ctypes.create_unicode_buffer(window_title_len)
        
        # Write to buffer
        ctypes.windll.user32.GetWindowTextW(window_handle, buffer, window_title_len)
        
        # Print the window title
        window_title = buffer.value

        #If window changes:
        if old_window_title != window_title:
            if (old_window_title == target_window):
                elapsed_time = time.time() - start_time
                print(f"Focused on {old_window_title} for {elapsed_time}")
                start_time = time.time()
            old_window_title = window_title

            print("SCREEN FLASH")

           


        


        # Wait for a short duration before checking again
        time.sleep(1)
            




if __name__ == "__main__":
    main()