import ctypes
from ctypes import windll, wintypes
from uuid import UUID
import winreg

def reformat_guid(in_guid, rule):
    out_guid = ""
    if rule == "msi_component":
        out_guid = in_guid[1:9][::-1] + \
                 in_guid[10:14][::-1] + \
                 in_guid[15:17][::-1] + \
                 in_guid[17:19][::-1] + \
                 in_guid[20:22][::-1] + \
                 in_guid[22:24][::-1] + \
                 in_guid[25:27][::-1] + \
                 in_guid[27:29][::-1] + \
                 in_guid[29:31][::-1] + \
                 in_guid[31:33][::-1] + \
                 in_guid[33:35][::-1] + \
                 in_guid[35:37][::-1]
    print("reformating GUID from {} to {}.".format(in_guid, out_guid))
    return out_guid

def get_knownfolderid(folder):
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ] 

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    KNOWNFOLDERID_GUID = {
        "ProgramFilesX64": "{6D809377-6AF0-444b-8957-A3773F02200E}",
        "ProgramFilesCommonX64": "{6365D5A7-0F0D-45E5-87F6-0DA56B6A4F7D}"
    }
    return _get_known_folder_path(KNOWNFOLDERID_GUID[folder])

def get_registry_root(registry_key):
    registry_roots = {
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER
    }
    return registry_roots[registry_key.split("\\")[0]]

def get_registry_key(registry_key):
    return registry_key[registry_key.find("\\"):-1]