import os
import jinja2
import tempfile
from PyPDF2 import PdfFileReader
from .page import Page

class TableOfContent:
    i = 1

    def __init__(self, project):
        self.project = project
        self.title = "Table of content"
        self.template = "table_of_content"
        self.overlay_template = ''
        self.position = 0

        self.apply_config()

        self.pdf_reader = self.get_pdf_reader()
        self.pages = self.get_pages()

    def apply_config(self):
        self.config = self.project.config
        toc_config_json = self.config.get_toc_config_json()

        if "title" in toc_config_json:
            self.title = toc_config_json["title"]

        if "template" in toc_config_json:
            self.template = toc_config_json["template"]

        if "overlay_template" in toc_config_json:
            self.overlay_template = toc_config_json["overlay_template"]

        if "position" in toc_config_json:
            self.position = int(toc_config_json["position"])


    def insert(self):
        self.project.documents.insert(self.position,self)

    def get_pdf_reader(self):
        items = self.get_toc_items()
        rendered_html = self.render(title = self.title, items = items)

        return self.build(rendered_html)

    def get_toc_items(self):
        items = []

        for document in self.project.documents:
            if not document.show_in_toc:
                continue

            line = f"{document.number:>4}. {document.title:.<60}{document.pages[0].full_number:.>10}"
            line = line.replace(" ","&nbsp;")
            items.append(line) 

        return items

    def render(self,**kwargs):
        environment = jinja2.Environment()
        template = environment.from_string(self.get_template())

        rendered = template.render(**kwargs)

        return rendered

    def build(self, html):
        num = __class__.i
        __class__.i += 1

        system_temp_dir = tempfile.gettempdir()
        program_temp_dir = os.path.join(system_temp_dir, "ReportBuilder")

        if not os.path.isdir(program_temp_dir):
            os.mkdir(program_temp_dir)

        template_file_path = os.path.join(program_temp_dir,"table_of_content.html")
        overlay_file_path = os.path.join(program_temp_dir,f"table_of_content{num}.pdf")

        with open(template_file_path, "w") as f:
            f.write(html)

        # wkhtmltox_file_path = "third-party\\wkhtmltox\\wkhtmltopdf.exe"
        wkhtmltox_file_path = "c:\\wkhtmltox\\wkhtmltopdf.exe"

        if not os.path.exists(wkhtmltox_file_path):
            raise FileNotFoundError(f"Can't find file: {wkhtmltox_file_path}")

        os.system(
        f"{wkhtmltox_file_path} "
        f"--log-level warn "
        f"--enable-local-file-access "
        f"--margin-bottom 30 --margin-top 30 --margin-left 0 --margin-right 0 "
        f"{template_file_path} "
        f"{overlay_file_path}"
        )

        toc_reader = PdfFileReader(open(overlay_file_path, 'rb'))

        return toc_reader

    def get_template(self):
        templates_dir = os.path.join("ReportBuilder", "templates")
        template_filename = f"{self.template}.html"
        template_file_path = os.path.join(templates_dir, template_filename)

        if not os.path.exists(template_file_path):
            raise FileNotFoundError(f"Can't find file: {template_filename}")

        with open(template_file_path, encoding="utf-8") as f:
            html = f.read()   

        return html

    def get_pages(self):
        result = []

        for i in range(len(self.pdf_reader.pages)):
            page = Page(self.pdf_reader, i)
            result.append(page)

        return result

    @property
    def info(self):
        info_dict = {
            "title" : self.title,
            "template" : self.overlay_template
        }
        return info_dict