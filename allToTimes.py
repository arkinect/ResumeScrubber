from pdfminer.layout import LTTextBoxHorizontal


def getLayout(docName):
    from pdfminer.layout import LAParams
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.layout import LTTextBoxHorizontal

    document = open(docName, 'rb')

    # Create resource manager
    rsrcmgr = PDFResourceManager()

    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(document):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()

    return layout


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


def writeToPdf(text, font, size, pdf, indent, hasDot):

    if text.strip() != "":
        style = ""
        if "BOLD" in font.upper():
            # print("line has bold")
            style = style + "B"
        if "ITALIC" in font.upper():
            # print("line has italic")
            style = style + "I"

        adapt = 0
        if hasDot:
            text = " - " + text
            adapt = 0

        pdf.set_font("Times", style=style, size=size)

        if indent-45-adapt > 0:
            pdf.cell(indent-45-adapt)
        pdf.multi_cell(0, 6, txt=text, border=0, align='L')



if __name__ == "__main__":
    from os import remove
    from fpdf import FPDF

    # output to text file
    outTxt = open("outTxt", 'w', encoding="utf-8")


    # extract info from pdfs
    docName = "Sherry Yang Resume.pdf"
    name = extractNames(docName)
    layoutTree = getLayout(docName)

    # create output pdf
    outPdf = FPDF()
    outPdf.set_left_margin(10)
    outPdf.set_right_margin(10)
    outPdf.add_page()

    for pdfObject in layoutTree:
        if isinstance(pdfObject, LTTextBoxHorizontal):
            for textLine in pdfObject:
                if (name[0] in textLine.get_text()) or (name[1] in textLine.get_text()):
                    pass
                    # print("censored for name")
                elif '@' in textLine.get_text():
                    pass
                    # print("censored for @")
                elif "linkedin" in textLine.get_text():
                    pass
                    # print("censored for linkedin")
                else:
                    for char in textLine:
                        font = char.fontname
                        fontSize = char.size
                        indent = char.bbox[0]
                        break
                    hasDot = False
                    if "\u25cf" in textLine.get_text():
                        hasDot = True

                    writeToPdf(textLine.get_text().encode("latin-1", "ignore").decode(), font, fontSize, outPdf, indent, hasDot)
                    outTxt.write(textLine.get_text())


    outPdf.output(docName[0:len(docName)-4] + " scrubbed.pdf")
