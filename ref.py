import os, sys, json

class ReferenceManager():
    def __init__(self):
        self.config_file = "ref.conf"
        self.config = {}
    
    def LoadConfig(self, config_file=None):
        if config_file:
            self.config_file = config_file
        if not os.path.isfile(self.config_file):
            print("[Error]: {} is not exists.".format(self.config_file))
            return
        with open(self.config_file) as in_file:
            self.config = json.load(in_file)

    def AddReferences(self):
        pass

    def ReduceReferences(self):
        pass

    def GetListToDelete(self):
        pass