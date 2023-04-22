import os
import sys

from logging_setup import get_logger

logger = get_logger(__name__)

sys.path.append("/opt/homebrew/lib/python3.11/site-packages")
from fpdf import FPDF


class DeviceReportGenerator:
    def __init__(self, devices):
        self.devices = devices

    def generate_report(self):
        report = ""
        for device in self.devices:
            report += f"Device {device['ip']}:\n"
            report += f"\tMAC Address: {device['mac']}\n"
            report += f"\tVendor: {device['vendor']}\n"
            report += f"\tHostname: {device['hostname']}\n"
            report += f"\tDevice Type: {device['device_type']}\n\n"
        return report


class PDFReport(FPDF):

    def __init__(self):
        super().__init__()
        self.logo_path = "logo.png"

    def header(self):

        self.image(self.logo_path, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'IoTShield Report', 0, 0, 'C')
        self.ln(20)

    def footer(self):

        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def create_report(self, data, filename):

        self.add_page()
        self.set_font("Arial", size=12)

        for item in data:
            self.cell(200, 10, txt=item, ln=True)

        if not os.path.exists("reports"):
            os.makedirs("reports")

        self.output(f"reports/{filename}")

class ReportGenerator:
    def __init__(self, devices):
        self.devices = devices

    def generate_report(self):
        device_report_generator = DeviceReportGenerator(self.devices)
        report_data = device_report_generator.generate_report()
        pdf_report = PDFReport()
        pdf_report.create_report(report_data.split('\n'), "IoTShield Report.pdf")
