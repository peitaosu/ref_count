import os, sys, json, winreg, re
from utils import reformat_guid, get_knownfolderid


class ReferenceManager():
    def __init__(self):
        self.config_file = "ref.conf"
        self.config = {}
        self.msi_key_string = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\"
    
    def LoadConfig(self, config_file=None):
        if config_file:
            self.config_file = config_file
        if not os.path.isfile(self.config_file):
            print("[Error]: {} is not exists.".format(self.config_file))
            sys.exit(-1)
        with open(self.config_file) as in_file:
            self.config = json.load(in_file)

    def _add_count_in_registry(self, component, product, file):
        try:
            component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,  + reformat_guid(component, "msi_component"), 0, winreg.KEY_SET_VALUE)
        except WindowsError:
            component_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, self.msi_key_string + reformat_guid(component, "msi_component"))
        for match in re.findall(r'(\[\{(\w+)\}\])', file):
            file = file.replace(match[0], get_knownfolderid(match[1]))
        winreg.SetValueEx(component_key, reformat_guid(product, "msi_component"), 0, winreg.REG_SZ, file)
        winreg.CloseKey(component_key)
        return True

    def _reduce_count_in_registry(self, component, product):
        try:
            component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.msi_key_string + reformat_guid(component, "msi_component"), 0, winreg.KEY_SET_VALUE)
        except WindowsError:
            return True
        try:
            winreg.DeleteValue(component_key, reformat_guid(product, "msi_component"))
            winreg.CloseKey(component_key)
            return True
        except WindowsError as e:
            print(e)
            return False

    def _get_count_in_registry(self, component):
        component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.msi_key_string + reformat_guid(component, "msi_component"))
        count = 0
        try:
            while 1:
                name, value, type = winreg.EnumValue(component_key, count)
                count = count + 1
        except WindowsError as e:
            print(e)
            return count

    def _delete_count_in_registry(self, component, product):
        try:
            component_key = winreg.OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Autodesk\\" + reformat_guid(product, "msi_component"), 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(component_key, reformat_guid(product, "msi_component")) 
            winreg.CloseKey(component_key)
            return True
        except WindowsError as e:
            print(e)
            return False
        
    def _remove_files(self, to_delete):
        for reference in to_delete:
            file = reference["File"]
            for match in re.findall(r'(\[\{(\w+)\}\])', file):
                file = file.replace(match[0], get_knownfolderid(match[1]))
            os.remove(file)
            for registry in reference["Registry"]:
                if len(reference["Registry"][registry]) == 0:
                    try:
                        registry_key = winreg.OpenKey(reference["Registry"][registry], 0, winreg.KEY_ALL_ACCESS)
                        winreg.DeleteKey(registry_key)
                    except WindowsError as e:
                        print(e)
                else:
                    for value in reference["Registry"][registry]:
                        try:
                            registry_key = winreg.OpenKey(reference["Registry"][registry], 0, winreg.KEY_ALL_ACCESS)
                            winreg.DeleteValue(registry_key, value)
                        except WindowsError as e:
                            print(e)

    def AddReferences(self):
        for reference in self.config["References"]:
            print("[Info]: Adding reference count for {}.".format(self.config["References"][reference]["File"]))
            if not self._add_count_in_registry(reference, self.config["ProductCode"], self.config["References"][reference]["File"]):
                print("[Error]: Adding reference count for {} failed.".format(self.config["References"][reference]["File"]))

    def ReduceReferences(self):
        for reference in self.config["References"]:
            print("[Info]: Reducing reference count for {}.".format(self.config["References"][reference]["File"]))
            if not self._reduce_count_in_registry(reference, self.config["ProductCode"]):
                print("[Error]: Reducing reference count for {} failed.".format(self.config["References"][reference]["File"]))

    def GetListToDelete(self):
        to_delete = []
        for reference in self.config["References"]:
            if _get_count_in_registry(reference) == 0:
                to_delete.append(reference)
        return to_delete
    
    def Install(self):
        self.AddReferences()
    
    def Uninstall(self):
        self.ReduceReferences()
        return self.GetListToDelete()

if __name__=="__main__":
    refman = ReferenceManager()
    refman.LoadConfig()
    refman.Install()