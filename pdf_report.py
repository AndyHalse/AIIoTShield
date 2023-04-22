from fpdf import FPDF

from logging_setup import get_logger

logger = get_logger(__name__)


class PDFReport(FPDF):

    def __init__(self, logo_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_path = logo_path

    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "IoTShield Report", 0, 1, "C")
        self.image(self.logo_path, 10, 8, 33)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()), 0, 0, "C")

    def report_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)

    def report_data(self, data):
        self.set_font("Arial", "", 12)
        for line in data:
            self.cell(0, 6, line, 0, 1)

    def generate_report(self, title, data, output_path):
        self.add_page()
        self.report_title(title)
        self.report_data(data)
        self.output(output_path)

# Example usage:
# pdf = PDFReport("logo.png")
# pdf.generate_report("Network Devices", ["Device 1", "Device 2"], "report.pdf")
