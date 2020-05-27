import os, sys, json, winreg, re
from utils import reformat_guid


class ReferenceManager():
    def __init__(self):
        self.config_file = "ref.conf"
        self.config = {}
    
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
            component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\" + reformat_guid(component), 0, winreg.KEY_WRITE)
            for match in re.findall(r'(\[\{(\w+)\}\])', file):
                file = file.replace(match[0], get_knownfolderid(match[1]))
            winreg.SetValueEx(component_key, reformat_guid(product), 0, winreg.REG_SZ, file)
            winreg.CloseKey(component_key)
            return True
        except WindowsError:
            return False

    def _reduce_count_in_registry(self, component, product):
        try:
            component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\" + reformat_guid(component), 0, winreg.KEY_WRITE)
            winreg.DeleteValue(component_key, reformat_guid(product))
            winreg.CloseKey(component_key)
            return True
        except WindowsError:
            return False

    def _get_count_in_registry(self, component):
        component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\" + reformat_guid(component))
        count = 0
        try:
            while 1:
                name, value, type = winreg.EnumValue(component_key, count)
                count = count + 1
        except WindowsError:
            return count

    def _delete_count_in_registry(self, component, product):
        try:
            component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\" + reformat_guid(component), 0, winreg.KEY_WRITE)
            winreg.DeleteValue(component_key, reformat_guid(product)) 
            winreg.CloseKey(component_key)
            return True
        except WindowsError:
            return False
        

    def AddReferences(self):
        for reference in self.config["References"]:
            if not self._add_count_in_registry(reference, self.config["ProductCode"], self.config["References"][reference]["File"]):
                print("[Error]: Adding reference count for {} failed.".format(self.config["References"][reference]["File"]))

    def ReduceReferences(self):
        for reference in self.config["References"]:
            if not self._reduce_count_in_registry(reference, self.config["ProductCode"]):
                print("[Error]: Reduce reference count for {} failed.".format(self.config["References"][reference]["File"]))

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
        to_delete = self.GetListToDelete()
        for to_delete_item in to_delete:
            os.remove(self.config["References"][to_delete_item]["File"])

if __name__=="__main__":
    refman = ReferenceManager()
    refman.Install()