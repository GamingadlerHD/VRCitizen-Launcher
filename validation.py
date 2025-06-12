import ctypes
from ctypes import wintypes
import os

from i18n import translate

def fits_on_any_monitor(width, height):
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # System DPI aware

    class MONITORINFOEX(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", wintypes.RECT),
            ("rcWork", wintypes.RECT),
            ("dwFlags", wintypes.DWORD),
            ("szDevice", wintypes.WCHAR * 32),
        ]

    monitor_sizes = []

    def callback(hMonitor, hdc, lprcMonitor, lParam): # pylint: disable=unused-argument
        mi = MONITORINFOEX()
        mi.cbSize = ctypes.sizeof(MONITORINFOEX)
        ctypes.windll.user32.GetMonitorInfoW(hMonitor, ctypes.byref(mi))
        w = mi.rcMonitor.right - mi.rcMonitor.left
        h = mi.rcMonitor.bottom - mi.rcMonitor.top
        monitor_sizes.append((w, h))
        return 1

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        wintypes.HMONITOR,
        wintypes.HDC,
        ctypes.POINTER(wintypes.RECT),
        ctypes.c_double
    )

    ctypes.windll.user32.EnumDisplayMonitors(
        0, 0,
        MonitorEnumProc(callback),
        0
    )

    return any(w >= width and h >= height for w, h in monitor_sizes)

def CheckPathsReturnInfo(scFolder, rsiPath, vorpxPath):
    if os.path.basename(os.path.normpath(scFolder)) != "LIVE":
        return False, translate("iName_sc_folder")
    if not os.path.isfile(os.path.join(rsiPath, "RSI Launcher.exe")):
        return False, translate("iName_rsi_launcher")
    if not os.path.isfile(os.path.join(vorpxPath, "vorpXcontroll.exe")):
        return False, translate("iName_vorpx")
    return True, ""

    
