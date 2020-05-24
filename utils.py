import win32com.client

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
    return out_guid

def _get_knownfolderid(self, folder):
    KNOWNFOLDERID = {
        "[{ProgramFilesX64}]": shellcon.FOLDERID_ProgramFilesX64
    }
    return shell.SHGetFolderPath(0, KNOWNFOLDERID[folder], None, 0)
