from utils.iniFile_utils import update_or_add_ini_property, add_item_to_list_if_needed
from constants import VORPCONTROL_INI, VORPX_INI



def SetVirtualDisplaySettings(bEnable, bManualAttach, bNoDisplayAttach, bHeadsetActivityAttach, customResolution=None):
    section = 'VirtualDisplay'
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bEnable', bEnable)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bManualAttach', bManualAttach)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bNoDisplayAttach', bNoDisplayAttach)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bHeadsetActivityAttach', bHeadsetActivityAttach)
    print(customResolution)

# def update_headset_settings(headsetType):
#     return

def AddExcludeIfNeeded():
    add_item_to_list_if_needed('RSI Launcher.exe', VORPCONTROL_INI)
    add_item_to_list_if_needed('StarCitizen_Launcher.exe', VORPCONTROL_INI)


# def check_exe_version(exe_path, version):
#     return False

# def update_vorpx():
#     return

def UpdateToDefaultKeyMappings():
    section = 'KeyMappings'
    defaultKeyMappings = {
        'iKeyMenu': 46,
        'iKeyEdgePeek': 4,
        'iKeyVRHotkeys': 260,
        'iKeyReset': 813,
        'iKeyCursor': 0,
        'iKeyStereoDisable': 0,
        'iKeyFovAdjust': 0,
        'iKeyCenterPosTracking': 800,
        'iKeyCenterGamepad': 0,
        'iKeyInfoOverlay': 0,
        'iKeyMagnifier': 4,
        'iKeyG3DZ3DSwitch': 0,
        'iKeyDvrScan': 0,
        'iKeyDvrEnable': 0
    }

    for key, value in defaultKeyMappings.items():
        update_or_add_ini_property(VORPX_INI, section, key, value)
