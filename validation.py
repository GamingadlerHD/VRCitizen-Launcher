import ctypes
from ctypes import wintypes
import os

from i18n import translate
from logs import log, warn

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
        log(f"Found monitor: {w}x{h}")
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
    log(f"Validating paths - SC: {scFolder}, RSI: {rsiPath}, VorpX: {vorpxPath}")
    
    if os.path.basename(os.path.normpath(scFolder)) != "LIVE":
        warn(f"Star Citizen folder validation failed: {scFolder}")
        return False, translate("iName_sc_folder")
    
    rsi_launcher_path = os.path.join(rsiPath, "RSI Launcher.exe")
    if not os.path.isfile(rsi_launcher_path):
        warn(f"RSI Launcher not found at: {rsi_launcher_path}")
        return False, translate("iName_rsi_launcher")
    
    vorpx_control_path = os.path.join(vorpxPath, "vorpXcontroll.exe")
    if not os.path.isfile(vorpx_control_path):
        warn(f"VorpX controller not found at: {vorpx_control_path}")
        return False, translate("iName_vorpx")
    
    log("All path validations passed successfully")
    return True, ""

    
