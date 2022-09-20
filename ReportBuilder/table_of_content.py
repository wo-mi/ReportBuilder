import os
import jinja2
from PyPDF2 import PdfReader
from .page import Page

class TableOfContent:
    i = 1

    def __init__(self, project):
        self.project = project
        self.config = self.project.config
        self.title = self.config.get(
                            "Table of content",
                            self.config.table_of_content["title"])
        self.template = self.config.get(
                            "table_of_content",
                            self.config.table_of_content["template"])
        self.overlay_template = self.config.get(
                            "",
                            self.config.table_of_content["overlay_template"])
        self.position = self.config.get(
                            0,
                            self.config.table_of_content["position"])

        self.pdf_reader = self.get_pdf_reader()
        self.pages = self.get_pages()

    def insert(self):
        self.project.documents.insert(self.position,self)

    def get_pdf_reader(self):
        items = self.get_table_of_content_items()
        rendered_html = self.render(title = self.title, items = items)

        return self.build(rendered_html)

    def close(self):
        try:
            self.pdf_reader.stream.close()
            self.pdf_reader = None
        except Exception as e:
            raise Exception("Cant close reader stream")

    def get_table_of_content_items(self):
        items = []

        for document in self.project.documents:
            if not document.show_in_toc:
                continue

            line = f"{document.number:>3}. {document.title:.<55}" \
                    f"{document.pages[0].full_number:.>10}"
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

        program_temp_dir = os.path.join(self.config["USER_DIR_PATH"], "Temp")

        if not os.path.isdir(program_temp_dir):
            os.makedirs(program_temp_dir)

        template_file_path = os.path.join(program_temp_dir,"table_of_content.html")
        overlay_file_path = os.path.join(program_temp_dir,f"table_of_content{num}.pdf")

        with open(template_file_path, "w") as f:
            f.write(html)

        wkhtmltox_file_path = self.config["WKHTMLTOPDF_PATH"]

        if not os.path.exists(wkhtmltox_file_path):
            basedir = os.path.dirname(os.path.abspath(__file__))
            wkhtmltox_file_path = os.path.join(basedir,"third-party\\wkhtmltopdf.exe")
            # raise FileNotFoundError(f"Can't find file: {wkhtmltox_file_path}")

        os.system(
        f"{wkhtmltox_file_path} "
        f"--log-level warn "
        f"--enable-local-file-access "
        f"--margin-bottom 40 --margin-top 40 --margin-left 0 --margin-right 0 "
        f"{template_file_path} "
        f"{overlay_file_path}"
        )

        toc_reader = PdfReader(open(overlay_file_path, 'rb'))

        return toc_reader

    def get_template(self):
        basedir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(basedir, "templates")
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
