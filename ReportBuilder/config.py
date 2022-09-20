import os
import json
from collections import UserDict
import tempfile

class Config(UserDict):

    default = {   
        "USER_DIR_PATH" : os.path.join(tempfile.gettempdir(), "ReportBuilder"),
        "WKHTMLTOPDF_PATH" : "c:\\wkhtmltox\\wkhtmltopdf.exe"
        }

    def __init__(self):
        self.data = {}

    def from_dict(self,dictionary):
        self.data.update(dictionary)

    def from_json_string(self, json_string):
        try:
            json_string_parsed = json.loads(json_string)
            self.data.update(json_string_parsed)
        except Exception:
            raise Exception("Can't parse json string")

    def from_file(self, path):
        if not os.path.exists(path):
            raise Exception("File doesn't exist")

        with open(path,"r") as f:
            json_string = f.read()

            try:
                json_string_parsed = json.loads(json_string)
                self.data.update(json_string_parsed)
            except Exception:
                raise Exception("Can't parse json string")

    def clear(self):
        self.data = {}

    def get(self, default=None, *args):
        for arg in args:
            if arg is not None:
                return arg

        return default

    @property
    def table_of_content(self):
        return self.__getitem__("table_of_content")

    @property
    def documents(self):
        return self.__getitem__("documents")


    def __getitem__(self,key):
        try:
            if type(self.data[key]) == dict: 
                conf = Config()
                conf.from_dict(self.data[key])
                return conf
            else:
                return self.data[key]

        except Exception as e:
            if key in self.default:
                return self.default[key]
            else:
                return None

