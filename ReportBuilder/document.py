import os
from PyPDF2 import PdfReader
import re
from .page import Page

class Document():
    def build_from_file(self, path, filename=None, config=None):
        self.number = 0
        self.path = path

        if filename is None:
            self.filename = os.path.basename(self.path)
        else:
            self.filename = filename

        self.config = config

        self.title = self.config.get(
                        self.filename,
                        self.config.documents[self.filename]["title"])
        self.overlay_template = self.config.get(
                        "", 
                        self.config.documents[self.filename]["overlay_template"],
                        self.config["overlay_template"])
        self.show_in_toc = self.config.get(
                        True,
                        self.config.documents[self.filename]["show_in_toc"])
        self.number_prefix = self.config.get(
                        "",
                        self.config.documents[self.filename]["number_prefix"])
        self.number_suffix = self.config.get(
                        "",
                        self.config.documents[self.filename]["number_suffix"])
        
        try:
            self.start_number = int(self.config.documents[self.filename]["start_number"])
        except:
            self.start_number = None

        self.pdf_reader = self.get_pdf_reader()

        self.origin_number_of_pages = self.get_pdf_number_of_pages()
        self.origin_pages = self.get_origin_pages()

        self.target_range_start = 0
        self.target_range_end = self.origin_number_of_pages

        self.interpret_target_range_string(self.config.documents[self.filename]["part"])

    def get_pdf_number_of_pages(self):
        return len(self.pdf_reader.pages)

    def interpret_target_range_string(self,strng):
        if strng is None:
            return None

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
        try:
            return PdfReader(open(self.path, "rb"))
        except Exception as e:
            raise Exception("Incorrect file")

    def close(self):
        try:
            self.pdf_reader.stream.close()
            self.pdf_reader = None
        except Exception as e:
            raise Exception("Cant close reader stream")

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
