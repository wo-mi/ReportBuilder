# ReportBuilder

This application allows to create a final technical report composed of many partial reports which come in PDF format from various third-party software.

### Some of the essential features are:
- Adding additional custom overlay layer to source PDF files in order to hide or change unwanted parts of source document (for example add company header and footer).
- Creating a table of contents based on included documents.
- Full customization of every page of the output report.
- Full control over pages numbering.
- Creating additional custom HTML templates for overlay layer and table of contents (using jinja template engine).
- Merging automatically PDF files within the project.
- Allowing to create and maintain following revisions of a project.
- Slicing source PDF files for extracting only required parts.
- Support for any PDF page size.


### Picture 1. PDF header from source document:
![alt text](docs/pic1.png "Source PDF header")
### Picture 2. PDF header overwritten by HTML template:
![alt text](docs/pic2.png "Target PDF header")

---

### Picture 3. Automatic and fully customizable table of contents:
![alt text](docs/pic3.png "Automatic table of contents")
