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
            sys.exit(-1)
        with open(self.config_file) as in_file:
            self.config = json.load(in_file)

    def _add_count_in_registry(self, component, product, file):
        pass

    def AddReferences(self):
        for reference in self.config["References"]:
            self._add_count_in_registry(reference, self.config["ProductCode"], self.config["References"][reference]["File"])

    def ReduceReferences(self):
        pass

    def GetListToDelete(self):
        pass