import os
from PyPDF2 import PdfWriter, PdfReader

class Overlay:
    def __init__(self):
        os.system("third-party\\wkhtmltox\\wkhtmltopdf.exe --margin-bottom 0 --margin-top 0 --margin-left 0 --margin-right 0 ReportBuilder\\templates\\default.html ReportBuilder\\tmp\\overlay.pdf")
        self.overlay()


    def overlay(self):
        # minutesFile = open('output.pdf', 'rb')
        reader = PdfReader('example_project\\document 1.pdf')
        writer = PdfWriter()    
        
        
        
        minutesFirstPage = reader.pages[0]
        pdfWatermarkReader = PdfReader(open('ReportBuilder\\tmp\\overlay.pdf', 'rb'))
        minutesFirstPage.merge_page(pdfWatermarkReader.pages[0],True)
        
        # print(minutesFirstPage.get('/Rotate'))

        writer.addPage(minutesFirstPage)

        for pageNum in range(1, reader.numPages):
            pageObj = reader.getPage(pageNum)
            writer.addPage(pageObj)
            
        # resultPdfFile = open('watermarkedCover.pdf', 'wb')
        # pdfWriter.write(resultPdfFile)
        # minutesFile.close()
        # resultPdfFile.close()

        with open('watermarkedCover.pdf', "wb") as fp:
            writer.write(fp)