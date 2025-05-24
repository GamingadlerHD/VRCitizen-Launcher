
<p align="center">
  <img src="./media/logo1.png" width="200" alt="Star Citizen Logo"/>
</p>

# VRCitizenLauncher

**VRCitizenLauncher** is a custom VR-friendly launcher for **Star Citizen** that simplifies setting up the game for use with headsets like the Meta Quest series via **vorpX**. It automates configuration, preserves system integrity, and offers powerful user customization.

---

## 💡 Features

- 🎯 **Headset Templates** – Predefined FOV and resolution settings for headsets like Quest 2 and others.
- 🛠 **Game Configuration Editor** – Adjust Star Citizen's `attributes.xml` directly.
- 🔭 **Aspect Ratio Lock** – When using templates, width/height adjust dynamically to preserve correct display.
- 🎮 **Automatic Launch Sequence** – One-click launch after initial setup.
- 🔐 **EAC Bypass Automation** – Automatically disables Easy Anti-Cheat and restores it afterward.
- 🧩 **Hook Helper Injection** – Automatically adds `dxgi.dll` for vorpX compatibility.
- 🧼 **Manual and Automatic Reset** – All changes to hostfile, game files, and system state are cleanly reverted after exit or if an error occurs.
- 📜 **GUI & Console Versions** – Use either `VRCitizenLauncher.exe` (no console) or `VRCitizenLauncher-debug.exe` (with visible console for debugging).
- 🌍 **Multilanguage Support** – Locales folder including English, German, Italian, Spanish and Russian

---

## 🚀 Getting Started

1. **Download the latest release** from the [Releases](https://github.com/yourusername/VRCitizenLauncher/releases) tab.
2. Extract the `.zip` archive.
3. Run `VRCitizenLauncher.exe` (or the debug version for logging).
4. If needed get the dxgi.dll and add it to the Launcher folder.
5. Follow the instructions on the launcher interface:
   - Select your **Star Citizen folder (LIVE)**.
   - Point to your **vorpX executable**.
   - Select the **Launcher executeable**
   - The app will automatically find your software if it is installed in the default path.
   - Customize resolution or FOV if desired.
   - Click **Launch** and enjoy in VR!

---

## 📁 Folder Structure

```

VRCitizenLauncher/
├── VRCitizenLauncher.exe
├── VRCitizenLauncher-debug.exe
├── templates.json
├── locales/
│   └── ...
└── logo.png

```

---

## ⚠️ Disclaimer

This launcher is intended **only for use with the LIVE version** of Star Citizen.  
Modifying files or bypassing systems on **PTU or other branches** is strictly prohibited and may violate the Terms of Service of the game. Use responsibly and at your own risk.

---

## 📩 Feedback / Issues

Please report issues or suggestions via the [Issues](https://github.com/GamingadlerHD/VRCitizen-Launcher/issues) tab.

---

