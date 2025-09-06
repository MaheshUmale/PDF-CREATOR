import os
import io
import re
import gdown
from googleapiclient.discovery import build
from PyPDF2 import PdfMerger

# --- SCRIPT SETUP ---
# NOTE: This script requires the 'gdown' and 'PyPDF2' libraries.
# You can install them by running:
# pip install gdown PyPDF2
# It also requires a Google Cloud project with the Docs API enabled to parse the links.
# 1. Go to the Google Cloud Console: https://console.cloud.google.com/
# 2. Create a new project.
# 3. Go to "APIs & Services" -> "Library" and enable "Google Docs API".
# 4. Go to "APIs & Services" -> "Credentials" -> "Create Credentials" -> "API Key".
# 5. Copy the generated API key.

# --- CONFIGURATION ---
# Replace this with the ID of your main Google Doc (the table of contents).
# You can find the ID in the URL of the document.
MASTER_DOC_ID = 'YOUR_MASTER_DOC_ID_HERE'

# Replace this with your Google Cloud API Key.
API_KEY = 'YOUR_API_KEY_HERE'

# --- HELPER FUNCTIONS ---

def get_linked_doc_ids(docs_service, master_doc_id):
    """
    Parses the master document to find all Google Docs links and extracts their IDs.
    Returns a list of tuples: [(doc_id, title), ...]
    """
    print("Parsing master document for chapter links...")
    doc = docs_service.documents().get(documentId=master_doc_id).execute()
    content = doc.get('body').get('content')
    linked_docs = []

    for element in content:
        if 'paragraph' in element:
            paragraph = element.get('paragraph')
            for run in paragraph.get('elements'):
                if 'textRun' in run:
                    text_run = run.get('textRun')
                    text = text_run.get('content')
                    
                    if 'link' in text_run.get('textStyle', {}):
                        link_url = text_run['textStyle']['link']['url']
                        
                        # Use a regular expression to extract the Google Doc ID from the URL.
                        match = re.search(r'/d/([a-zA-Z0-9_-]+)', link_url)
                        if match:
                            doc_id = match.group(1)
                            title = text.strip().replace('\n', '')
                            if doc_id and title:
                                print(f"  Found chapter: '{title}' with ID: {doc_id}")
                                linked_docs.append((doc_id, title))
    
    return linked_docs

def download_doc_as_pdf(doc_id, doc_title, output_dir='pdfs'):
    """
    Downloads a single Google Doc as a PDF file using gdown.
    Returns the path to the downloaded PDF.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"{doc_title.replace(' ', '_')}.pdf")
    print(f"\nDownloading '{doc_title}' as PDF using gdown...")
    
    # gdown automatically handles the conversion of a Google Doc to PDF.
    gdown.download(id=doc_id, output=file_path, quiet=False, fuzzy=True)
    
    print(f"  Successfully downloaded to '{file_path}'")
    return file_path

def merge_pdfs(pdf_paths, output_filename='Ebook_Combined.pdf'):
    """Merges a list of PDF files into a single output PDF."""
    print(f"\nMerging {len(pdf_paths)} PDFs into '{output_filename}'...")
    merger = PdfMerger()
    
    for pdf_path in pdf_paths:
        try:
            merger.append(pdf_path)
            print(f"  Appended {os.path.basename(pdf_path)}")
        except Exception as e:
            print(f"  Error appending {pdf_path}: {e}")
            
    merger.write(output_filename)
    merger.close()
    
    print(f"\nSuccessfully created the final ebook: '{output_filename}'")
    
# --- MAIN SCRIPT EXECUTION ---

if __name__ == '__main__':
    # Build the Docs service to parse links. This requires an API key.
    docs_service = build('docs', 'v1', developerKey=API_KEY)
    
    # 1. Get the list of chapter documents from the master doc
    linked_docs = get_linked_doc_ids(docs_service, MASTER_DOC_ID)
    
    if not linked_docs:
        print("No Google Docs links found in the master document. Please ensure the links are present and accessible.")
    else:
        # 2. Download each chapter as a PDF
        downloaded_pdfs = []
        for doc_id, doc_title in linked_docs:
            try:
                pdf_path = download_doc_as_pdf(doc_id, doc_title)
                downloaded_pdfs.append(pdf_path)
            except Exception as e:
                print(f"Error downloading {doc_title}: {e}")
        
        if downloaded_pdfs:
            # 3. Merge the downloaded PDFs into a single file
            merge_pdfs(downloaded_pdfs)
