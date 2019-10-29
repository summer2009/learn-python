import camelot
filename = '2015.pdf'
num = 4
#tables = camelot.read_pdf(filename,str(num))
tables = camelot.read_pdf(filename,'1-10')
print('numOfTables = ',len(tables))

if len(tables)>0:
    for table in tables:
        print("-"*100)
        #print(table.df.iloc[0])
        #print(table.df[0])
        #print(table.df)
        print(table.df.shape)
        print(table.parsing_report)
        #input()

# 根据table首行和首列中的文字信息提取识别表格主要内容
# caption of row
print(table.df.iloc[0])
# caption of col
print(table.df[0])

# caption of table


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


# Open a PDF file.
#filename = '2016.pdf'
fp = open(filename, 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
document = PDFDocument(parser,'')
#Check if the document allows text extraction. If not, abort.
#if not document.is_extractable:
#    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
#device = PDFDevice(rsrcmgr)

laparams = LAParams()
device = PDFPageAggregator(rsrcmgr,laparams=laparams)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
numOfPage = 1
txtOfThisPage = ''
for page in PDFPage.create_pages(document):
    #应该使用各种方法识别当前页的tables，综合后确定当前页的tables
    tablesInCurPageLattice = camelot.read_pdf(filename,str(numOfPage))
    numOFTablesInCurPageL = len(tablesInCurPageLattice)
    print('numOFTablesInCurPageL = ',numOFTablesInCurPageL)
    
    tablesInCurPageStream = camelot.read_pdf(filename,str(numOfPage),flavor='stream')
    numOFTablesInCurPageS = len(tablesInCurPageStream)
    print('numOFTablesInCurPageS = ',numOFTablesInCurPageS)
                
    interpreter.process_page(page)
    layout = device.get_result()
    
    txtList = []          
       
    for x in layout:
        if isinstance(x, LTTextBox):
            #将所有LTTextBox中text保存为list，便于table合并和查找caption
            txtList.append(x.get_text().strip())
            #txtOfThisPage += x.get_text().strip()
    
    print(txtList)
    
    if numOFTablesInCurPageL > 0:
        for table in tablesInCurPageLattice:
            #获取当前table的caption
            
            #判断table中第一个元素在list中的位置，应将table.df[0][0]进行处理，去除'\n'及其之后的字符
            firstElement = table.df[0][0].find('\n')
            tmpStr = ''
            if firstElement != -1:
                tmpStr = table.df[0][0]
                print('tmpStr = ',tmpStr)
                tmpStr = tmpStr[0:firstElement]
            else:
                tmpStr = table.df[0][0]
            
            
            if txtList.count(tmpStr) > 0:
                indexOfCaption = txtList.index(tmpStr) - 1
                if indexOfCaption >= 0:
                    print('tableCaption = ',txtList[indexOfCaption])
            print("-"*100)
            print(table.df)
            
    if numOFTablesInCurPageS > 0:
        for table in tablesInCurPageStream:
            #获取当前table的caption
            
            #判断table中第一个元素在list中的位置，应将table.df[0][0]进行处理，去除'\n'及其之后的字符
            firstElement = table.df[0][0].find('\n')
            tmpStr = ''
            if firstElement != -1:
                tmpStr = table.df[0][0]
                print('tmpStr = ',tmpStr)
                tmpStr = tmpStr[0:firstElement]
            else:
                tmpStr = table.df[0][0]
            
            
            if txtList.count(tmpStr) > 0:
                indexOfCaption = txtList.index(tmpStr) - 1
                if indexOfCaption >= 0:
                    print('tableCaption = ',txtList[indexOfCaption])
            print("-"*100)
            print(table.df)
    
    
    
    print('numOfPage = ',numOfPage)        
    numOfPage = numOfPage + 1
    print("*"*120)
    #input()
