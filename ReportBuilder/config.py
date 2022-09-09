import os
import json


class Config:
    def __init__(self):
        self.data = None

    def load_from_file(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("Can't find project config file: " \
                                                f"{path}")

        try:
            with open(path) as f:
                self.data = json.load(f)
        except Exception as e:
            print("Can't parse config file...")

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

    def get_toc_config_json(self):
        if "table_of_content" in self.data:
            toc_config = self.data["table_of_content"]
            return toc_config
        else:
            return None
