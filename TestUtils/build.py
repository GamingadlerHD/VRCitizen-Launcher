import os
import shutil

import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name', 'RSI Launcher',
    '--onefile',
    '--noconsole',
    'MockApp.py',
])

PyInstaller.__main__.run([
    '--name', 'vorpControl',
    '--onefile',
    '--noconsole',
    'MockApp.py',
])

PyInstaller.__main__.run([
    '--name', 'StarCitizen',
    '--onefile',
    '--noconsole',
    'MockApp.py',
])

data = {
    'sc_entry': "sc_entry",
    'vorpx_entry': "vorpx_entry",
    'launcher_entry': "launcher_entry",
    'fov_entry': 120,
    'width_entry': 1799,
    'height_entry': 1284,
    'stay_in_vr': False,
    'use_dxgi': True,
    'template_dropdown': "Test",
    'preset_dropdown': "Test",
    'ign_res_warning': True,
    'additional_popup': False,
    "keep_keybinds": False,
    "custom_config": False
}

# Define source and destination paths
file_mappings = {
    # exe files from ./dist
    './dist/vorpControl.exe': './Files/VorpX/vorpControl.exe',
    './dist/RSI Launcher.exe': './Files/Game/RSI Launcher/RSI Launcher.exe',
    './dist/StarCitizen.exe': './Files/Game/StarCitizen/Bin64/StarCitizen.exe',
    # other files from ./TestFiles
    './TestFiles/vorpControl.ini': './Files/VorpX/vorpControl.ini',
    './TestFiles/vorpX.ini': './Files/VorpX/vorpX.ini',
    './TestFiles/GenericHMD.ini': './Files/VorpX/Devices/Display/GenericHMD.ini',
    './TestFiles/attributes.xml': './Files/Game/StarCitizen/user/client/0/Profiles/default/attributes.xml',
}

for src, dst in file_mappings.items():
    dst_dir = os.path.dirname(dst)
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)







# Mocks
class MockUiElement:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value
    
class AlwaysTrueDict:
    class AlwaysFalseElement:
        def get(self):
            return 0

    def __getitem__(self, key):
        if key == "HeadtrackingSource":
            class HeadtrackingSourceElement:
                def get(self):
                    return "Tobi"
            return HeadtrackingSourceElement()
        return self.AlwaysFalseElement()