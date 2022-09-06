import os
import json
from PyPDF2 import PdfReader, PdfWriter
import re

CONFIG_FILENAME = "config.json"

class Project:

    def __init__(self, path):
        self.title = os.path.basename(path)
        # self.template = "default"
        self.documents = []
        
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
            if filename == CONFIG_FILENAME:
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

    def get_project_info(self):
        info_dict = {
            "title" : self.title,
            "path" : self.path
        }

        return info_dict

    def number_documents(self):
        i = 1
        for document in self.documents:
            document.number = i
            document.number_pages()
            i+=1


    # def merge_project(self):
    #     writer = PdfWriter()

    #     for document in self.documents:
    #         for page in document.target_pages:
    #             overlay = document.get_overlay()
    #             if overlay is None:
    #                 writer.addPage(page)

    #             else:
    #                 page.merge_page(overlay,True)
    #                 writer.addPage(page)

    #     with open('output.pdf', 'wb') as f:
    #         writer.write(f)


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


class Document():
    def __init__(self, path):
        self.number = 0
        self.path = path
        self.filename = os.path.basename(self.path)
        self.title = self.filename
        self.template = "default"
        self.config = None
        self.origin_number_of_pages = self.get_origin_document_number_of_pages()

        self.target_range_start = 0        
        self.target_range_end = self.origin_number_of_pages
        
        # self.apply_config()


        #self.pages = self.get_target_pages()

    def apply_config(self, config):
        self.config = config
        document_config_json = self.config.get_document_config_json(self.filename)

        if "title" in document_config_json:
            self.title = document_config_json["title"]

        if "template" in document_config_json:
            self.template = document_config_json["template"]

        if "part" in document_config_json:
            range_strng = document_config_json["part"]
            self.interpret_target_range_string(range_strng)

    def get_origin_document_number_of_pages(self):
        reader = PdfReader(self.path)
        return len(reader.pages)

        # for page in reader.pages:
        #     width = int(page.mediabox[2])
        #     height = int(page.mediabox[3])
        #     self.origin_page_sizes.append((width,height))

    def interpret_target_range_string(self,strng):
        pattern = re.compile("^\[\d*:\d*]$")
        if not pattern.match(strng):
            raise SyntaxError("Wrong part range syntax")

        start, end = strng[1:-1].split(":")
        if start == "":
            start = 0
        else:
            start = int(start)

        if end == "":
            end = self.origin_number_of_pages
        else:
            end = int(end)

        self.target_range_start = start        
        self.target_range_end = end

    # def get_origin_document_reader(self):
    #     return PdfReader(self.path)
    # def get_overlay(self):
    #     if self.template == "":
    #         print("asdasdad")            
    #         return None
    #     else:
    #         print("asd")
    #         overlay = Overlay()
    #         return overlay.get_reader()

    def get_document_info(self):
        info_dict = {
            "path" : self.path,
            "filename" : self.filename,
            "title" : self.title,
            "template" : self.template
        }

        return info_dict

    def get_target_page_info(self, page_nr):
        pass

    # @property
    # def target_pages(self):
    #     reader = PdfReader(self.path)
    #     result = []

    #     for i in range(len(reader.pages)):
    #         if i in range(self.target_range_start,self.target_range_end):
    #             result.append(reader.pages[i])

    #     return result

    # def __str__(self):
    #     return f"{self.title} {self.origin_number_of_pages}"

    @property
    def pages(self):
        reader = PdfReader(self.path)
        result = []

        for i in range(len(reader.pages)):
            if i in range(self.target_range_start,self.target_range_end):
                page = Page(reader.pages[i])
                result.append(page)

        return result

    def number_pages(self):
        i=1
        for page in self.pages:
            page.number = i
            i+=1


    def __str__(self):
        return f"{self.title} {self.origin_number_of_pages}"


class Page:
    def __init__(self, reader_page):
        self.number = 0
        self.reader_page = reader_page

        self.width = int(reader_page.mediabox[2])
        self.height = int(reader_page.mediabox[3])


class TableOfContent:
    pass


class Config:
    def __init__(self, path):

        self.path = os.path.join(path, CONFIG_FILENAME)        
        if not self.has_config_file():
            raise FileNotFoundError("Can't find project config file " \
                                                f"{CONFIG_FILENAME}")  

        self.data = {}

        self.parse_config_file()

    # def get(self, key):
    #     if key in self.data:
    #         return self.data[key]
    #     else:
    #         return None


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
