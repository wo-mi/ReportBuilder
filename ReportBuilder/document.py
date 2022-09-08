import os
from PyPDF2 import PdfFileReader
import re
from .page import Page

class Document():
    def __init__(self, path):
        self.number = 0
        self.path = path
        self.filename = os.path.basename(self.path)
        self.title = self.filename
        self.overlay_template = "default"
        self.config = None
        self.start_number = None
        self.number_prefix = ""
        self.number_suffix = ""
        self.show_in_toc = True

        self.pdf_reader = self.get_pdf_reader()     
           
        self.origin_number_of_pages = self.get_pdf_number_of_pages()

        self.target_range_start = 0        
        self.target_range_end = self.origin_number_of_pages
        
        self.origin_pages = self.get_origin_pages()

    def apply_config(self, config):
        self.config = config
        document_config_json = self.config.get_document_config_json(self.filename)

        if "title" in document_config_json:
            self.title = document_config_json["title"]

        if "overlay_template" in document_config_json:
            self.overlay_template = document_config_json["overlay_template"]

        if "part" in document_config_json:
            range_strng = document_config_json["part"]
            self.interpret_target_range_string(range_strng)

        if "number_prefix" in document_config_json:
            self.number_prefix = document_config_json["number_prefix"]

        if "number_suffix" in document_config_json:
            self.number_suffix = document_config_json["number_suffix"]

        if "start_number" in document_config_json:
            self.start_number = int(document_config_json["start_number"])

        if "show_in_toc" in document_config_json:
            if document_config_json["show_in_toc"].lower() == "false":
                self.show_in_toc = False

    def get_pdf_number_of_pages(self):
        return len(self.pdf_reader.pages)

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
    
    def get_pdf_reader(self):
        return PdfFileReader(open(self.path, "rb"))

    def get_origin_pages(self):
        result = []

        for i in range(len(self.pdf_reader.pages)):
            page = Page(self.pdf_reader, i)
            result.append(page)

        return result

    def number_pages(self, last=0):
        if self.start_number is None:
            i = last            
        else:
            i = self.start_number - 1
        
        for page in self.pages:
            i+=1
            page.number = i
            page.number_prefix = self.number_prefix
            page.number_suffix = self.number_suffix

        return i

    @property
    def pages(self):
        result = []

        for i, page in enumerate(self.origin_pages):
            if i in range(self.target_range_start,self.target_range_end):
                result.append(page)

        return result

    @property
    def info(self):
        info_dict = {
            "path" : self.path,
            "filename" : self.filename,
            "title" : self.title,
            "template" : self.overlay_template
        }
        return info_dict

    def __str__(self):
        return f"{self.title}"