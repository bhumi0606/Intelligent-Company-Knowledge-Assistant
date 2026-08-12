from pypdf import PdfReader
import docx

# function for extract pdf file
def extract_pdf(filename):
    reader = PdfReader(filename)
    pages = []

    for i, page in enumerate(reader.pages,start=1):
        text = page.extract_text()
        if text:
            pages.append({"page_number":i,"text":text})

    return pages

# function for extract docx file
def extract_docx(filename):
    reader = docx.Document(filename)
    paragraphs = []
    for paragraph in reader.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    text = "\n".join(paragraphs)
    if not text:
        return []

    return [{"page_number":1, "text": text}]

# function for extract txt file
def extract_txt(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    if not text.strip():
        return []
    return [{"page_number":1, "text": text}]

# function for calling extract text
def extract_text(filename):
    lower_filename = filename.lower()

    if lower_filename.endswith(".pdf"):
        return extract_pdf(filename)
    if lower_filename.endswith(".txt"):
        return extract_txt(filename)
    if lower_filename.endswith(".docx"):
        return extract_docx(filename)

    raise ValueError(f"Unsupported file type:{filename}")