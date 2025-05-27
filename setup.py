import shutil
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name', 'VRCitizenLauncher',
    '--onefile',
    '--noconsole',
    '--icon', 'media/i.ico',
    'main.py',
])

PyInstaller.__main__.run([
    '--name', 'VRCitizenLauncher-Debug',
    '--onefile',
    '--icon', 'media/i.ico',
    'main.py',
])

# coppy files dist folder
shutil.copy2('templates.json', 'dist/templates.json')

# coppy locales folder to dist folder
shutil.copytree('locales', 'dist/locales', dirs_exist_ok=True)
shutil.copytree('media', 'dist/media', dirs_exist_ok=True)
 
