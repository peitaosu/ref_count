import win32com.client
from win32com.shell import shellcon, shell

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
    KNOWNFOLDERID = {
        "[{ProgramFilesX64}]": shellcon.FOLDERID_ProgramFilesX64
    }
    return shell.SHGetFolderPath(0, KNOWNFOLDERID[folder], None, 0)
