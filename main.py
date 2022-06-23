def pdfToText(pdfPath):
    from io import StringIO
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfparser import PDFParser

    output_string = StringIO()
    with open(pdfPath, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        in_file.close()

    return output_string.getvalue()


def writeToTxt(textToClean, docName):
    newDocName = docName[0:len(docName)-4] + ".txt"

    newText = open(newDocName, "w", encoding="utf-8")  # creates blank txt doc
    newText.write(textToClean.encode("latin-1", "ignore").decode())  # pastes in text from resume
    newText.close()  # closes doc
    newText = open(newDocName, "r", encoding="utf-8")  # opens new text doc to be read
    newTextLines = newText.readlines()  # reads lines into list
    newText.close()  # closes doc
    newText = open(newDocName, "w", encoding="utf-8")
    newText.truncate(0)
    name = extractNames(docName)
    for line in newTextLines:
        if (name[0] not in line) and (name[1] not in line) and ("@" not in line) and ("linkedin" not in line):
            newText.write(line)
    newText.close()


def extractNames(docName):
    for i in range(len(docName)):
        if docName[i] == " ":
            break
    firstName = docName[0: i]

    for j in range(i + 1, len(docName)):
        if docName[j] == " ":
            break
    lastName = docName[i + 1: j]

    return firstName, lastName


def txtToPdf(docName):
    from os import remove
    from fpdf import FPDF

    outPdf = FPDF()
    outPdf.add_page()
    outPdf.set_font("Arial", size=12)
    toPdf = open(docName[0:len(docName)-4] + ".txt", "r", encoding="utf-8")

    for line in toPdf:
        outPdf.cell(200, 10, txt=line, ln=1, align='L')

    toPdf.close()
    remove(docName[0:len(docName)-4] + ".txt")
    outPdf.output(docName[0:len(docName)-4] + " scrubbed.pdf")


if __name__ == "__main__":
    path = "Mathew Lane Resume.pdf"
    pdfText = pdfToText(path)
    # print(pdfText)
    writeToTxt(pdfText, path)
    txtToPdf(path)


