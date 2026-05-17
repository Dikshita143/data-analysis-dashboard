from fpdf import FPDF
import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sales, Employee & Customer Data Analysis', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_metric(self, label, value):
        self.set_font('Arial', 'B', 11)
        self.cell(40, 10, f"{label}:", 0, 0)
        self.set_font('Arial', '', 11)
        self.cell(0, 10, f"{value}", 0, 1)

def generate_pdf_summary(data_summary, output_path):
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.chapter_title("Executive Summary")
    pdf.chapter_body("This report provides an overview of the business performance across Sales, Employee, and Customer domains.")
    
    for section, metrics in data_summary.items():
        pdf.chapter_title(section)
        for label, value in metrics.items():
            pdf.add_metric(label, str(value))
        pdf.ln(5)
    
    pdf.output(output_path)
    return output_path
