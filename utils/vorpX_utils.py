import os
from logs import log, error, warn
from utilities import kill_process_by_name, wait_for_exit
from utils.iniFile_utils import update_or_add_ini_property, add_item_to_list_if_needed
from constants import VORPCONTROL_INI, VORPX_INI, GENERICHMD_INI
from templates import GetTemplateByName

async def PrepareVorpX(vorpXpath: str, headsetName: str, useCustomVXConfig = False, keepKeybinds : bool = False):
    log(f"Preparing VorpX - Path: {vorpXpath}, Headset: {headsetName}, Custom Config: {useCustomVXConfig}, Keep Keybinds: {keepKeybinds}")

    changed = False
    if not keepKeybinds:
        if UpdateToDefaultKeyMappings():
            log("Key mappings updated successfully")
            changed = True
    if AddExcludeIfNeeded():
        log("Exclusion settings updated")
        changed = True
    if not useCustomVXConfig:
        if UpdateHeadsetSettings(headsetName):
            log("Headset settings updated successfully")
            changed = True
    if changed:
        log("VorpX configuration changed, restarting VorpX process")
        kill_process_by_name(os.path.basename(vorpXpath))
        await wait_for_exit(os.path.basename(vorpXpath))

def SetVirtualDisplaySettings(bEnable, bManualAttach, bNoDisplayAttach, bHeadsetActivityAttach, customResolution=None):
    log(f"Setting virtual display settings - Enable: {bEnable}, Manual: {bManualAttach}, NoDisplay: {bNoDisplayAttach}, Headset: {bHeadsetActivityAttach}")
    
    section = 'VirtualDisplay'
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bEnable', bEnable)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bManualAttach', bManualAttach)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bNoDisplayAttach', bNoDisplayAttach)
    update_or_add_ini_property(VORPCONTROL_INI, section, 'bHeadsetActivityAttach', bHeadsetActivityAttach)
    
    if customResolution:
        log(f"Custom resolution provided: {customResolution}")
    else:
        log("No custom resolution specified")

def UpdateHeadsetSettings(headsetName: str):
    template = GetTemplateByName(headsetName)
    
    if not template:
        warn(f"No template found for headset: {headsetName}")
        return False
        
    try:
        if template['headsetType'].startswith('GenericHMD'):
            splitedHeadsetSettings = template['headsetType'].split(';')
            log(f"GenericHMD settings: {splitedHeadsetSettings}")

            res1 = update_or_add_ini_property(VORPX_INI, 'General', 'sDeviceIniName', splitedHeadsetSettings[0])
            res2 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iRecommendedHmdResX', splitedHeadsetSettings[1])
            res3 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iRecommendedHmdResY', splitedHeadsetSettings[2])
            res4 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iScreenResX', splitedHeadsetSettings[1])
            res5 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'iScreenResY', splitedHeadsetSettings[2])
            res6 = update_or_add_ini_property(GENERICHMD_INI, 'Hardware', 'fDisplayCamFovV', template['fov'])
            
            changes_made = any([res1, res2, res3, res4, res5, res6])
            log(f"GenericHMD settings update completed, changes made: {changes_made}")
            return changes_made
        log(f"Processing standard headset template: {template['headsetType']}")
        res = update_or_add_ini_property(VORPX_INI, 'General', 'sDeviceIniName', template['headsetType'])
        return res
    except Exception as e:
        error(f"ECL1500: Template '{headsetName}' processing failed. Error: {e}")
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
        'iKeyMenu': 46,
        'iKeyEdgePeek': 4,
        'iKeyVRHotkeys': 260,
        'iKeyReset': 813,
        'iKeyCenterPosTracking': 800,
        'iKeyCenterGamepad': 0,
        'iKeyInfoOverlay': 0,
        'iKeyMagnifier': 4,
        'iKeyG3DZ3DSwitch': 0,
        'iKeyDvrScan': 0,
        'iKeyDvrEnable': 0,
        'iKeyCursor': 0,
        'iKeyStereoDisable': 0,
        'iKeyFovAdjust': 0,
    }

    changed = False
    updated_count = 0

    for key, value in defaultKeyMappings.items():
        key_updated = update_or_add_ini_property(VORPX_INI, section, key, value)
        if key_updated:
            updated_count += 1
            changed = True

    log(f"Key mappings update completed - {updated_count} keys updated, total changes: {changed}")
    return changed
