import time
import ctypes

def hide_console():
    # This will hide the console window (Windows only)

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

hide_console()

while True:
    # Infinite loop that does minimal work
    time.sleep(1)