import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    '--name', 'VRCitizenLauncher',
    '--onefile',
    '--noconsole',
    'main.py',
])

PyInstaller.__main__.run([
    '--name', 'VRCitizenLauncher-Debug',
    '--onefile',
    'main.py',
])
