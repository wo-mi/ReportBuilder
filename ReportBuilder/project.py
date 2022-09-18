import os, shutil
from .document import Document
from .page import Page
from .table_of_content import TableOfContent
from .config import Config
from .merger import Merger


CONFIG_FILENAME = "config.json"

class Project:

    def __init__(self):
        self.title = "Default"
        self.documents = []
        self.output_filename = "Default"

    def build_from_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"Wrong path to project folder: {dir_path}")

        self.title = os.path.basename(dir_path)
        self.output_filename = os.path.basename(dir_path)

        self.config = Config()
        self.config.load_from_file(os.path.join(dir_path, CONFIG_FILENAME))

        self.load_documents_from_dir(dir_path)

        self.build()

    def build_from_database(self, config, files_list):

        self.config = Config()
        self.config.load_from_string(config)

        self.load_documents_from_list(files_list)

        self.build()

    def build(self):
        self.apply_config()

        self.set_documents_in_order()

        self.number_documents()

        self.table_of_content = TableOfContent(self)
        self.table_of_content.insert()

    def load_documents_from_dir(self, dir_path):
        filenames = os.listdir(dir_path)

        for filename in filenames:
            if filename == CONFIG_FILENAME:
                continue
            if filename.startswith("."):
                continue

            document = Document()
            document_path = os.path.join(dir_path, filename)
            document.build_from_file(document_path)

            self.documents.append(document)

        if len(self.documents) == 0:
            raise Exception("No document files")

    def load_documents_from_list(self, files_list):
        for file in files_list:
            filename = file[0]
            file_path = file[1]

            if not os.path.exists(file_path):
                raise Exception("Wrong document path")
            
            document = Document()
            document.build_from_file(path=file_path, filename=filename)

            self.documents.append(document)

        if len(self.documents) == 0:
            raise Exception("No document files")

    def open_documents(self):
        for document in self.documents:
            document.open()

    def close_documents(self):
        for document in self.documents:
            document.close()

    def apply_config(self):

        if "title" in self.config.data:
            self.title = self.config.data["title"]

        if "output_filename" in self.config.data:
            self.output_filename = self.config.data["output_filename"]

        if "overlay_template" in self.config.data:
            for document in self.documents:
                document.overlay_template = self.config.data["overlay_template"]

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
            if document.show_in_toc:
                document.number = i
                i+=1

        last_page_number = 0
        for document in self.documents:
            last_page_number = document.number_pages(last_page_number)

    def merge(self):
        merger = Merger(self)
        self.temp_output_pdf_path = merger.merge()

    def save(self,dir_path=""):
        destination = os.path.join(dir_path, f"{self.output_filename}.pdf")
        shutil.move(self.temp_output_pdf_path, destination)
        return os.path.abspath(destination)

    @property
    def info(self):
        info_dict = {
            "title" : self.title
        }
        return info_dict

    def __str__(self):
        strng = f"Project: '{self.title}'\n"

        first_line = True
        for document in self.documents:
            if first_line:
                strng += f"Documents: '{document}'\n"
                first_line = False
            else:
                strng += f"           '{document}'\n"

        return strng
