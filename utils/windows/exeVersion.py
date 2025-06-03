import ctypes

def get_file_version(file_path):
    size = ctypes.windll.version.GetFileVersionInfoSizeW(file_path, None)
    if not size:
        return None

    res = ctypes.create_string_buffer(size)
    ctypes.windll.version.GetFileVersionInfoW(file_path, None, size, res)
    
    r = ctypes.c_void_p()
    l = ctypes.c_uint()
    ctypes.windll.version.VerQueryValueW(res, u'\\', ctypes.byref(r), ctypes.byref(l))
    
    if not r:
        return None

    class VS_FIXEDFILEINFO(ctypes.Structure):
        _fields_ = [
            ("dwSignature", ctypes.c_uint32),
            ("dwStrucVersion", ctypes.c_uint32),
            ("dwFileVersionMS", ctypes.c_uint32),
            ("dwFileVersionLS", ctypes.c_uint32),
            ("dwProductVersionMS", ctypes.c_uint32),
            ("dwProductVersionLS", ctypes.c_uint32),
            ("dwFileFlagsMask", ctypes.c_uint32),
            ("dwFileFlags", ctypes.c_uint32),
            ("dwFileOS", ctypes.c_uint32),
            ("dwFileType", ctypes.c_uint32),
            ("dwFileSubtype", ctypes.c_uint32),
            ("dwFileDateMS", ctypes.c_uint32),
            ("dwFileDateLS", ctypes.c_uint32),
        ]

    info = VS_FIXEDFILEINFO.from_address(r.value)

    major = info.dwFileVersionMS >> 16
    minor = info.dwFileVersionMS & 0xFFFF
    build = info.dwFileVersionLS >> 16
    revision = info.dwFileVersionLS & 0xFFFF

    return f"{major}.{minor}.{build}.{revision}"