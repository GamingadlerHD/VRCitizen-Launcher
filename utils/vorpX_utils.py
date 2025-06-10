import os
from utilities import kill_process_by_name
from utils.iniFile_utils import update_or_add_ini_property, add_item_to_list_if_needed
from constants import VORPCONTROL_INI, VORPX_INI, GENERICHMD_INI
from templates import GetTemplateByName

def PrepareVorpX(vorpXpath: str, headsetName: str, useCustomVXConfig = False, keepKeybinds : bool = False):

    changed = False
    if not keepKeybinds:
        if UpdateToDefaultKeyMappings():
            changed = True
    if AddExcludeIfNeeded():
        changed = True
    if not useCustomVXConfig:
        if UpdateHeadsetSettings(headsetName):
            changed = True
    if changed:
        kill_process_by_name(os.path.basename(vorpXpath))

def SetVirtualDisplaySettings(bEnable, bManualAttach, bNoDisplayAttach, bHeadsetActivityAttach, customResolution=None):
    section = 'VirtualDisplay'
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bEnable', bEnable)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bManualAttach', bManualAttach)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bNoDisplayAttach', bNoDisplayAttach)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bHeadsetActivityAttach', bHeadsetActivityAttach)
    print(customResolution)

def UpdateHeadsetSettings(headsetName: str):
    template = GetTemplateByName(headsetName)
    try:
        if template['headsetType'].startswith('GenericHMD'):
            splitedHeadsetSettings = template['headsetType'].split(';')
            print(splitedHeadsetSettings)

            res1 = update_or_add_ini_property(VORPX_INI, 'General', 'sDeviceIniName', splitedHeadsetSettings[0])
            res2 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iRecommendedHmdResX', splitedHeadsetSettings[1])
            res3 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iRecommendedHmdResY', splitedHeadsetSettings[2])
            res4 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iScreenResX', splitedHeadsetSettings[1])
            res5 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iScreenResY', splitedHeadsetSettings[2])
            res6 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'fDisplayCamFovV', template['fov'])
            return any([res1, res2, res3, res4, res5, res6])
        else:
            res = update_or_add_ini_property(VORPX_INI, 'General', 'sDeviceIniName', template['headsetType'])
            return res
    except AttributeError:
        print(f"Template '{headsetName}' not found.")
        return False

def AddExcludeIfNeeded():
    if add_item_to_list_if_needed('RSI Launcher.exe', VORPCONTROL_INI) or add_item_to_list_if_needed('StarCitizen_Launcher.exe', VORPCONTROL_INI):
        return True
    return False



# def check_exe_version(exe_path, version):
#     return False

# def update_vorpx():
#     return

def UpdateToDefaultKeyMappings():
    section = 'KeyMappings'
    defaultKeyMappings = {
    }

    # REMOVED FOR NOW

    changed = False

    for key, value in defaultKeyMappings.items():
        cn= update_or_add_ini_property(VORPX_INI, section, key, value)
        if cn: changed = True

    return changed
