import pdfplumber
import docx
from io import StringIO

# text/plain
# application/vnd.openxmlformats-officedocument.wordprocessingml.document
# application/pdf

def extract_txt_from_pdf(feed) -> str:
    # PDF a texto
    with pdfplumber.open(feed) as pdf:
        pages = pdf.pages
        for p in pages:
            txt = p.extract_text()
    return txt

def extrat_txt_from_docx(feed)-> str:
    # DOCX a texto
    doc = docx.Document(feed)
    lines = [para.text for para in doc.paragraphs]
    txt = "\n".join(lines)
    return txt

def extract_txt_from_txt(feed) -> str:
    # TXT a texto
    with StringIO(feed.getvalue().decode('utf-8')) as f:
        txt = f.read()
    return txt

def extract_data(datatxt) -> str:
    match datatxt.type:
        case "application/pdf":
            return extract_txt_from_pdf(datatxt)
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extrat_txt_from_docx(datatxt)
        case "text/plain":
            return extract_txt_from_txt(datatxt)
        case _:
            return "Tipo de archivo no soportado"
