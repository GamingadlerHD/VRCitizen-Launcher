from utils.iniFile_utils import update_ini_property
from constants import VORPCONTROL_INI, VORPX_INI



def update_vrtDis_settings(bEnable, bManualAttach, bNoDisplayAttach, bHeadsetActivityAttach, customResolution=None):
    section = 'VirtualDisplay'
    update_ini_property(VORPCONTROL_INI, section, 'bEnable', bEnable)
    update_ini_property(VORPCONTROL_INI, section, 'bManualAttach', bManualAttach)
    update_ini_property(VORPCONTROL_INI, section, 'bNoDisplayAttach', bNoDisplayAttach)
    update_ini_property(VORPCONTROL_INI, section, 'bHeadsetActivityAttach', bHeadsetActivityAttach)

def update_headset_settings(headsetType):
    return

def add_exclude_if_needed():
    return


def check_exe_version(exe_path, version):
    return False

def update_vorpx():
    return


