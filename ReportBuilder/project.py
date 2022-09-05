import os
import json

CONFIG_FILENAME = "config.json"

class Project:
    def __init__(self, path):
        self.title = os.path.basename(path)
        self.header_template = "default"
        self.footer_template = "default"
        self.documents = []
        
        if not os.path.isdir(path):
            raise NotADirectoryError("Wrong path to project folder")
        
        self.path = path

        if not self.has_config_file():
            raise FileNotFoundError("Can't find project config file " \
                                                f"{CONFIG_FILENAME}")

        self._config_path = os.path.join(self.path, CONFIG_FILENAME)

        self.parse_config_file()

        self.find_documents()


    def has_config_file(self):
        config_file_path = os.path.join(self.path, CONFIG_FILENAME)

        return os.path.exists(config_file_path)


    def parse_config_file(self):
        with open(self._config_path) as f:
            config_data = json.load(f)
        
        if "title" in config_data:
            self.title = config_data["title"]


    def find_documents(self):
        document_filenames_list = os.listdir(self.path)

        for document_filename in document_filenames_list:
            if document_filename == CONFIG_FILENAME:
                continue
            if document_filename.startswith("."):
                continue
        
            self.documents.append(document_filename)


    def __str__(self):
        strng = f"Project: '{self.title}'\n" \
                f"Path: '{self.path}'\n"

        first_line = True
        for document in self.documents:
            if first_line:
                strng += f"Documents: '{document}'\n"
                first_line = False
            else:
                strng += f"           '{document}'\n"                

        return strng


class Document:
    pass


class TableOfContent:
    pass