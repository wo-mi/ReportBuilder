import jinja2

class TableOfContent:
    def __init__(self, project):
        self.project = project
        self.title = "Table of content"

    def get_html(self):
        items = []

        for document in self.project.documents:
            line = f"{document.number:>4}. {document.title:.<50}{document.pages[0].full_number:.>10}"
            line = line.replace(" ","&nbsp;")
            items.append(line) 

        return self.render(title = self.title, items = items)

    def render(self,**kwargs):
        environment = jinja2.Environment()
        template = environment.from_string(self.template)

        rendered = template.render(**kwargs)

        return rendered

    @property
    def template(self):
        template_file_path = "ReportBuilder\\templates\\table_of_content.html"

        with open(template_file_path, encoding="utf-8") as f:
            html = f.read()

        return html