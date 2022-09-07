import os
from .document import Document
from .page import Page
from .table_of_content import TableOfContent
from .config import Config
from .merger import Merger

class Project:

    def __init__(self, path):
        self.title = os.path.basename(path)
        self.documents = []
        self.table_of_content = TableOfContent(self)

        if not os.path.isdir(path):
            raise NotADirectoryError("Wrong path to project folder")
        
        self.path = path

        self.config = Config(self.path)

        self.find_documents()

        self.apply_config()

        self.set_documents_in_order()

        self.number_documents()

    def find_documents(self):
        filenames = os.listdir(self.path)

        for filename in filenames:
            if filename == self.config.filename:
                continue
            if filename.startswith("."):
                continue

            document_path = os.path.join(self.path, filename)
            document = Document(document_path)

            self.documents.append(document)

    def apply_config(self):
        
        if "title" in self.config.data:
            self.title = self.config.data["title"]

        if "template" in self.config.data:
            for document in self.documents:
                document.template = self.config.data["template"]

        for document in self.documents:
            document.apply_config(self.config)

    def set_documents_in_order(self):
        result = []
        order_list = self.config.get_documents_order()
        
        for filename in order_list:
            for i in range(len(self.documents)):
                if filename == self.documents[i].filename:
                    result.append(self.documents.pop(i))
                    break
        
        result += self.documents
        self.documents = result

    def number_documents(self):
        i = 1
        for document in self.documents:
            document.number = i
            i+=1

        last_page_number = 0
        for document in self.documents:
            last_page_number = document.number_pages(last_page_number)
    
    def merge(self):
        merger = Merger(self)
        merger.merge()

    @property
    def info(self):
        info_dict = {
            "title" : self.title,
            "path" : self.path
        }
        return info_dict

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