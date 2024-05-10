from pyhtml2pdf import converter
#from weasyprint import HTML

converter.convert('http://127.0.0.1:8000/imops/Alc/2024-05-31/info/pdf', 'PDF/sample.pdf')

#document = HTML(url='http://127.0.0.1:8000/imops/Alc/2024-05-31/info/pdf')

#document.write_pdf('sample.pdf', stylesheets=["style.css"])  # Assuming 'style.css' has the @page rule