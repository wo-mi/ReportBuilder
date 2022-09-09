class Page:
    def __init__(self, reader, reader_page_number):
        self.number = 0
        self.number_prefix = ""
        self.number_suffix = ""

        self.reader = reader
        self.reader_page_number = reader_page_number

    def get(self):
        return self.reader.pages[self.reader_page_number]

    @property
    def width(self):
        return round(
            float(self.reader.pages[self.reader_page_number].mediabox.width)
            * (25.4/72))

    @property
    def height(self):
        return round(
            float(self.reader.pages[self.reader_page_number].mediabox.height) 
            * (25.4/72))

    @property
    def full_number(self):
        return f"{self.number_prefix}{self.number}{self.number_suffix}"

    @property
    def info(self):
        info_dict = {
            "number" : self.number,
            "full_number" : self.full_number,
            "width" : self.width,
            "height" : self.height
        }
        return info_dict
