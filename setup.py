import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    '--name', 'StarCitizenVRLauncher',
    '--onefile',
    '--noconsole',
    'main.py',
])
