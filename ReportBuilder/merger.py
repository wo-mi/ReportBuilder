import os
from PyPDF2 import PdfWriter, PdfReader
import jinja2
import subprocess

class Merger:

    def __init__(self, project):
        self.project = project
        self.templates = self.get_templates()

    def merge(self):
        writer = PdfWriter()

        for document in self.project.documents:
            print(f"Merging: '{document.title}'")

            for page in document.pages:
                print("#", end="")

                if document.template == "":
                    writer.addPage(page.reader_page)
                else:

                    if document.template not in self.templates:
                        raise AttributeError(f"Can't find template "
                                            "{document.template}")

                    template = self.templates[document.template]
                    template.render(page_number = page.number)

                    overlay = Overlay(template)
                    overlay_pdf = overlay.get()

                    page.reader_page.merge_page(overlay_pdf,True)
                    writer.addPage(page.reader_page)
            
            print()

        with open('output.pdf', 'wb') as f:
            writer.write(f)

    def get_templates(self):
        templates_dir = os.path.join("ReportBuilder", "templates")

        result = {}

        for template_filename in os.listdir(templates_dir):
            with open(os.path.join(templates_dir, template_filename)) as f:
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
        environment = jinja2.Environment()
        template = environment.from_string(self.html)

        rendered = template.render(**kwargs)

        path = "ReportBuilder\\tmp\\template.html"

        with open(path, "w") as f:
            f.write(rendered)


class Overlay:
    def __init__(self, template):
        self.template = template

    # def __new__(self):
        
        # os.system("third-party\\wkhtmltox\\wkhtmltopdf.exe --margin-bottom 0 --margin-top 0 --margin-left 0 --margin-right 0 ReportBuilder\\templates\\default.html ReportBuilder\\tmp\\overlay.pdf")
        # # self.overlay()
        # overlay_reader = PdfReader(open('ReportBuilder\\tmp\\overlay.pdf', 'rb'))
    
    def get(self):
        
        # subprocess.run(["third-party\\wkhtmltox\\wkhtmltopdf.exe",
        #  "--margin-bottom 0 --margin-top 0 --margin-left 0 --margin-right 0",
        #  "ReportBuilder\\tmp\\template.html",
        #  "ReportBuilder\\tmp\\overlay.pdf"])


        os.system(
        "third-party\\wkhtmltox\\wkhtmltopdf.exe "
        "--log-level warn "
        "--margin-bottom 0 --margin-top 0 --margin-left 0 --margin-right 0 "
        "ReportBuilder\\tmp\\template.html "
        "ReportBuilder\\tmp\\overlay.pdf"
        )

        overlay_reader = PdfReader(open('ReportBuilder\\tmp\\overlay.pdf', 'rb'))
        return overlay_reader.pages[0]

    # def overlay(self):
    #     # minutesFile = open('output.pdf', 'rb')
    #     reader = PdfReader('example_project\\document 1.pdf')
    #     writer = PdfWriter()    
        
        
        
    #     minutesFirstPage = reader.pages[0]
    #     pdfWatermarkReader = PdfReader(open('ReportBuilder\\tmp\\overlay.pdf', 'rb'))
    #     minutesFirstPage.merge_page(pdfWatermarkReader.pages[0],True)
        
    #     # print(minutesFirstPage.get('/Rotate'))

    #     writer.addPage(minutesFirstPage)

    #     for pageNum in range(1, reader.numPages):
    #         pageObj = reader.getPage(pageNum)
    #         writer.addPage(pageObj)
            
    #     # resultPdfFile = open('watermarkedCover.pdf', 'wb')
    #     # pdfWriter.write(resultPdfFile)
    #     # minutesFile.close()
    #     # resultPdfFile.close()

    #     with open('watermarkedCover.pdf', "wb") as fp:
    #         writer.write(fp)