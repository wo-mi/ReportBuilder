import os
import json

CONFIG_FILENAME = "config.json"


class Config:
    def __init__(self, path):
        self.filename = CONFIG_FILENAME
        self.path = os.path.join(path, CONFIG_FILENAME)        
        if not self.has_config_file():
            raise FileNotFoundError("Can't find project config file " \
                                                f"{CONFIG_FILENAME}")  

        self.data = {}

        self.parse_config_file()

    def get_document_config_json(self, filename):
        if "documents" in self.data:
            document_configs = self.data["documents"]  

            for document_config in document_configs:
                if "filename" not in document_config:
                    continue

                if filename in document_config["filename"]:
                    return document_config
        else:
            return None

    def get_documents_order(self):
        result = []
        if "documents" in self.data:
            document_configs = self.data["documents"]  

            for document_config in document_configs:
                if "filename" not in document_config:
                    continue
                    
                result.append(document_config["filename"])

        return result

    def parse_config_file(self):
        try:
            with open(self.path) as f:
                self.data = json.load(f)
        except Exception as e:
            print("Can't parse config file...")

        # if "title" in config_data:
        #     self.title = config_data["title"]

    def has_config_file(self):
        return os.path.exists(self.path)
