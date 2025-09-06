from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

def extract_hyperlinks_from_word(file_path):
    document = Document(file_path)
    hyperlinks = []

    for paragraph in document.paragraphs:
        if not paragraph.hyperlinks:
            continue
        for hyperlink in paragraph.hyperlinks:
            print(hyperlink.text)
            print(hyperlink.address)
            hyperlinks.append(hyperlink.address)
    # Also check document-level relationships for hyperlinks (e.g., in headers/footers)
    for rel in document.part.rels:
        if document.part.rels[rel].reltype == RT.HYPERLINK:
            hyperlinks.append(document.part.rels[rel].target_ref)
    return hyperlinks

# Example usage:
word_document_path = 'D:\\py_code_workspace\\PDF CREATOR\\index.docx'
extracted_links = extract_hyperlinks_from_word(word_document_path)
for link in extracted_links:
    print(link)