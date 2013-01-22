import json


class JsonConfig:
    def __init__(self, fname, config=None):
        self.fname = fname
        self.config = config

    def read(self):
        if self.config:
            return self.config
        with open(self.fname, "rb") as infile:
            config = json.load(infile)
            self.config = config
            return self.config

    def save(self, indent=None):
        with open(self.fname, "wb") as outfile:
            json.dump(self.config, outfile, indent=indent)
