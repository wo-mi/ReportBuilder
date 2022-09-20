import os
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader
import jinja2

class Merger:

    def __init__(self, project):
        self.project = project
        self.config = self.project.config
        self.templates = self.get_templates()

    def merge(self):
        writer = PdfWriter()

        for document in self.project.documents:
            print(f"Merging: '{document.title}'")

            for page in document.pages:
                print("#", end="")

                if document.overlay_template == "":
                    writer.add_page(page.get())
                else:

                    if document.overlay_template not in self.templates:
                        raise AttributeError(f"Can't find template "
                                            f"{document.template}")

                    template = self.templates[document.overlay_template]

                    context = {
                        'date' : datetime.now().strftime("%m.%d.%Y"),
                        'time' : datetime.now().strftime("%H:%M:%S"),
                        'datetime' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        }

                    html = template.render(context=context,
                                            project = self.project.info,
                                            document = document.info,
                                            page = page.info)

                    overlay = Overlay(self.config)
                    overlay_pdf = overlay.build(html, page)     

                    new_page = page.get()
                    new_page.merge_page(overlay_pdf,True)
                    writer.add_page(new_page)

            print()

        temp_output_pdf_path = self.save_temp_pdf(writer)

        return temp_output_pdf_path

    def save_temp_pdf(self, writer):
        writer.page_layout = "/SinglePage"

        program_temp_dir = os.path.join(self.config["USER_DIR_PATH"], "Temp")
        
        if not os.path.isdir(program_temp_dir):
            os.makedirs(program_temp_dir)

        output_file_temp_path = os.path.join(program_temp_dir, "output.pdf")

        with open(output_file_temp_path, 'wb') as f:
            writer.write(f)        

        return output_file_temp_path 


    def get_templates(self):
        basedir = os.path.dirname(os.path.abspath(__file__))

        templates_dir = os.path.join(basedir, "templates")

        result = {}

        for template_filename in os.listdir(templates_dir):
            if not os.path.splitext(template_filename)[1] == ".html":
                continue

            template_file_path = os.path.join(templates_dir, template_filename)

            with open(template_file_path, encoding="utf-8") as f:
                html = f.read()   

            template_name = os.path.splitext(template_filename)[0]

            template = Template(template_name, html)
            result[template_name] = template

        return result


class Template:
    def __init__(self, name, html):
        self.name = name
        self.html = html

    def render(self, **kwargs):
        basedir = os.path.dirname(os.path.abspath(__file__))

        environment = jinja2.Environment()

        func = lambda filename: "file:///" + os.path.join(
                        basedir, "templates", filename)

        environment.globals['image'] = func
        template = environment.from_string(self.html)

        rendered = template.render(**kwargs)

        return rendered


class Overlay:
    i = 1
    def __init__(self, config):
        self.config = config

    def build(self, html, page):
        num = __class__.i
        __class__.i += 1

        program_temp_dir = os.path.join(self.config["USER_DIR_PATH"], "Temp")

        if not os.path.isdir(program_temp_dir):
            os.makedirs(program_temp_dir)

        template_file_path = os.path.join(program_temp_dir,"overlay.html")
        overlay_file_path = os.path.join(program_temp_dir,f"overlay{num}.pdf")

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
        f"--page-width {page.width} --page-height {page.height} "
        f"--margin-bottom 0 --margin-top 0 --margin-left 0 --margin-right 0 "

        f"{template_file_path} "
        f"{overlay_file_path}"
        )

        overlay_reader = PdfReader(open(overlay_file_path, 'rb'))
        result = overlay_reader.pages[0]

        return result
