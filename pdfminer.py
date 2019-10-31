import camelot

#filename = '2015.pdf'
#tables = camelot.read_pdf(filename,'1-192')

filename = '2019q3.pdf'
tables = camelot.read_pdf(filename,'1-34')

#num = 4
#tables = camelot.read_pdf(filename,str(num))

print('numOfTables = ',len(tables))

if len(tables)>0:
    for table in tables:
        print("-"*100)
        tableReport = table.parsing_report
        print(tableReport)
        curTableShape = table.df.shape[1]
        print('curTableColNum = ',curTableShape)
        
        print('curTableInPage = ',tableReport['page'])       
        
        
        #print(table.df.iloc[0])
        #print(table.df[0])
        #print(table.df)
        #input()
if len(tables)>0:
    for index in range(len(tables) - 1,-1,-1):
        print("-"*100)
        tableReport = tables[index].parsing_report
        print(tableReport)
        curTableShape = tables[index].df.shape[1]
        print('curTableIndex = ',index)
        print('curTableColNum = ',curTableShape)        
        print('curTableInPage = ',tableReport['page'])      
        
        
        #print(table.df.iloc[0])
        #print(table.df[0])
        #print(table.df)
        #input()
        
# 根据table首行和首列中的文字信息提取识别表格主要内容
# caption of row
print(table.df.iloc[0])
# caption of col
print(table.df[0])

# caption of table


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage,PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
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
txtOfAllPages = []
for page in PDFPage.create_pages(document):
    #应该使用各种方法识别当前页的tables，综合后确定当前页的tables
    tablesInCurPageLattice = camelot.read_pdf(filename,str(numOfPage))
    numOFTablesInCurPageL = len(tablesInCurPageLattice)
    print('numOFTablesInCurPageL = ',numOFTablesInCurPageL)
    
    
    '''
    #stream 方式识别table错误过多，不适用
    tablesInCurPageStream = camelot.read_pdf(filename,str(numOfPage),flavor='stream')
    numOFTablesInCurPageS = len(tablesInCurPageStream)
    print('numOFTablesInCurPageS = ',numOFTablesInCurPageS)
    '''            
    
    interpreter.process_page(page)
    layout = device.get_result()
    
    txtList = []          
       
    for x in layout:
        if isinstance(x, LTTextBox):
            #将所有LTTextBox中text保存为list，便于table合并和查找caption
            txtList.append(x.get_text().strip())
            #txtOfThisPage += x.get_text().strip()
    
    print(txtList)
    
    txtOfAllPages.append(txtList)
    '''
    合并由于页面排版原因被切割开的table
    '''   
    
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
    
    print('numOfPage = ',numOfPage)        
    numOfPage = numOfPage + 1
    print("*"*120)
    #input()
print(txtOfAllPages)



'''
所有数据都已准备好，由后往前开始进行表合并
'''
if len(tables)>0:
    for index in range(len(tables) - 1,0,-1):
        print("-"*100)
        tableReport = tables[index].parsing_report     
        
        print(tableReport)
        curTableShape = tables[index].df.shape[1]
        print('curTableIndex = ',index)
        print('curTableColNum = ',curTableShape)        
        print('curTableInPage = ',tableReport['page'])
        
        
        preTableReport = tables[index - 1].parsing_report
        print(preTableReport)
        preTableShape = tables[index - 1].df.shape[1]
        print('preTableIndex = ',index - 1)
        print('preTableColNum = ',preTableShape)        
        print('preTableInPage = ',preTableReport['page'])
        
        # 当前table和前一个table列数不同，肯定不是一个table，无需合并
        if (preTableShape == curTableShape) & (preTableReport['page'] == (tableReport['page'] - 1)):
            print('可能需要table合并！！！！！')
            # 判断当前table是否是当前页top位置的元素，如果是：可能性更大，需要进一步判断pretable是否是前一页最底端元素，如果是，则合并
            print('###当前页文本：\n',txtOfAllPages[tableReport['page'] - 1])
            print('###前一页文本：\n',txtOfAllPages[preTableReport['page'] - 1])
            
            #判断table中第一个元素在list中的位置，应将table.df[0][0]进行处理，去除'\n'及其之后的字符
            firstElement = tables[index].df[0][0].find('\n')
            tmpStr = ''
            if firstElement != -1:
                tmpStr = tables[index].df[0][0]
                print('tmpStr = ',tmpStr)
                tmpStr = tmpStr[0:firstElement]
            else:
                tmpStr = tables[index].df[0][0]
            
            print('firstElement = ',tmpStr)
            if txtOfAllPages[tableReport['page'] - 1].count(tmpStr) > 0:
                indexOfFirstElement = txtOfAllPages[tableReport['page'] - 1].index(tmpStr)
                print('indexOfFirstElement =  ',indexOfFirstElement)
                if indexOfFirstElement <= 3:
                    print('很大可能需要合并table！！！indexOfFirstElement =  ',indexOfFirstElement)
                    print(tables[index - 1].shape)
                    #print(tables[index - 1].df[0][31])
                    lastElement = tables[index - 1].df[tables[index - 1].shape[1] - 1][tables[index - 1].shape[0] - 1].find('\n')
                    tmpStr = ''
                    if lastElement != -1:
                        tmpStr = tables[index - 1].df[tables[index - 1].shape[1] - 1][tables[index - 1].shape[0] - 1]
                        print('tmpStr = ',tmpStr)
                        tmpStr = tmpStr[0:lastElement]
                    else:
                        tmpStr = tables[index - 1].df[tables[index - 1].shape[1] - 1][tables[index - 1].shape[0] - 1]            
                    print('lastElement = ',tmpStr)
                    if txtOfAllPages[preTableReport['page'] - 1].count(tmpStr) > 0:
                        tailOfTxtList = txtOfAllPages[preTableReport['page'] - 1][len(txtOfAllPages[preTableReport['page'] - 1]) - 3:len(txtOfAllPages[preTableReport['page'] - 1]) - 1]
                        #indexOfLastElement = tailOfTxtList.index(tmpStr)
                        
                        if tailOfTxtList.count(tmpStr)  > 0:
                            print('indexOfLastElement =  ',tmpStr)
                            print('需要合并table！！！')
            
            
        #print(table.df.iloc[0])
        #print(table.df[0])
        #print(table.df)
        #input()
