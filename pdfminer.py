import camelot
filename = '2016.pdf'
num = 4
tables = camelot.read_pdf(filename,str(num))
print(len(tables))
if len(tables)>0:
    for table in tables:
        print(table.df)



import camelot
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.converter import PDFPageAggregator


filename = '2019h.pdf'
num = 4

# Open a PDF file.
fp = open(filename, 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
document = PDFDocument(parser)
# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
#device = PDFDevice(rsrcmgr)

laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
numOfPage = 1
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    layout = device.get_result()
    for x in layout:
        if isinstance(x, LTTextBox):
            print(x.get_text().strip())
    print('numOfPage = ',numOfPage)    
    tables = camelot.read_pdf(filename,str(numOfPage))
    print('lenOfTables = ',len(tables))
    numOfPage = numOfPage + 1
