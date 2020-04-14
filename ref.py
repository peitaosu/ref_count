import os, sys, json, winreg
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
        component_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Installer\\UserData\\S-1-5-18\\Components\\" + reformat_guid(component), 0, winreg.KEY_WRITE)
        winreg.SetValueEx(component_key, reformat_guid(product), 0, winreg.REG_SZ, file)
        winreg.CloseKey(component_key)

    def AddReferences(self):
        for reference in self.config["References"]:
            self._add_count_in_registry(reference, self.config["ProductCode"], self.config["References"][reference]["File"])

    def ReduceReferences(self):
        pass

    def GetListToDelete(self):
        pass