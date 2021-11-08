from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import logging
import os

# Regardless of warning
logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)
all_files = os.walk(os.getcwd())

pdf_files = []
for i in all_files:

    for each_file in i[2]:

        if os.path.splitext(each_file)[1] == '.pdf':  # Estimate whether the file is a 'txt' file based on the suffix

            each_file = os.path.join(i[0], each_file)

            pdf_files.append(each_file)
ca=0
for each_pdf_file in pdf_files:
    ca = ca+1
    device = PDFPageAggregator(PDFResourceManager(), laparams=LAParams())
    interpreter = PDFPageInterpreter(PDFResourceManager(), device)

    doc = PDFDocument()
    parser = PDFParser(open(each_pdf_file, 'rb'))
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    path = "d:\keywordsearching"
    txt_filename=os.path.join(path, str(ca) + '.txt')
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        with open(txt_filename, 'w', encoding="utf-8") as fw:
            print("num page:{}".format(len(list(doc.get_pages()))))
            for page in doc.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        results = x.get_text()
                        fw.write(results)

def print_pos(key_dict):
    keys = key_dict.keys()

    keys = sorted(keys)

    for each_key in keys:
        print('The keyword is mentioned in line: %s ，content：%s 。' % (each_key, str(key_dict[each_key])))


def pos_in_line(line, key): #Searching function
    pos = []

    begin = line.find(key)

    while begin != -1:
        pos.append(begin + 1)

        begin = line.find(key, begin + 1)

    return pos


def search_in_file(file_name, key):
    f = open(file_name, encoding='utf-8')

    count = 0  # Recording the lines

    key_dict = dict()  # The certain positions of the keyword

    for each_line in f:

        count += 1

        if key in each_line:
            pos = pos_in_line(each_line, key)  # The certain positions in each line

            key_dict[count] = each_line

    f.close()

    return key_dict


def search_files(key):
    all_files = os.walk(os.getcwd())

    txt_files = []

    for i in all_files:

        for each_file in i[2]:

            if os.path.splitext(each_file)[1] == '.txt':  # Estimate whether the file is a 'pdf' file based on the suffix

                each_file = os.path.join(i[0], each_file)

                txt_files.append(each_file)

    for each_txt_file in txt_files:

        key_dict = search_in_file(each_txt_file, key)

        if key_dict:

            print('================================================================')

            print('The file【%s】 contains the keyword【%s】' % (each_txt_file, key))


            print_pos(key_dict)


key = input('keyword：')



search_files(key)

