import os
import glob
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

myPath = 'C:\\PyCharm\\PycharmProjects\\convertToThePdf\\StufftoMerge\\'

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    #for page in range(pdf.getNumPages()): #everypage
    for page in range(44,48): #pages(start,stop)
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}_page_{}.pdf'.format(
            fname, page + 1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))

###Splits sheets
# if __name__ == '__main__':
#     path = 'FinancialStatement.pdf'
#     pdf_splitter(path)


def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    #file_handles = []

    for path in input_paths:
        pdf_merger.append(path)

    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)

###Merge all sheets in a folder
if __name__ == '__main__':
    paths = glob.glob(myPath+'*.pdf')
    paths.sort()
    merger('MergedStuff.pdf', paths)
