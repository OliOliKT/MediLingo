from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return ' '.join(text)


docx_file_path = '/Users/majastyrkandersen/Desktop/bispebjerg/interviews_merged.docx'


document_text = read_docx(docx_file_path)