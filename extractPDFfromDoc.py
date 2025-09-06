from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

# --- 1. Define custom styles for better formatting ---
def get_custom_styles():
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(name='BookTitle',
                              parent=styles['h1'],
                              fontSize=24,
                              leading=28,
                              spaceAfter=0.5 * inch,
                              alignment=TA_CENTER))

    # Chapter Title style
    styles.add(ParagraphStyle(name='ChapterTitle',
                              parent=styles['h2'],
                              fontSize=18,
                              leading=22,
                              spaceAfter=0.2 * inch,
                              spaceBefore=0.5 * inch,
                              keepWithNext=1)) # Keep chapter title on same page as first paragraph

    # Section/Subsection (if needed)
    styles.add(ParagraphStyle(name='Section',
                              parent=styles['h3'],
                              fontSize=14,
                              leading=16,
                              spaceAfter=0.1 * inch))

    # Normal text style
    styles.add(ParagraphStyle(name='BodyText',
                              parent=styles['Normal'],
                              fontSize=12,
                              leading=14,
                              spaceAfter=0.1 * inch,
                              firstLineIndent=0.25 * inch, # Indent first line of paragraphs
                              alignment=TA_LEFT))

    # Table of Contents entry style
    styles.add(ParagraphStyle(name='TOCEntry',
                              parent=styles['Normal'],
                              fontSize=12,
                              leading=14,
                              spaceAfter=0.05 * inch))
    return styles

# --- 2. Custom page template for headers/footers (including page numbers) ---
class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        SimpleDocTemplate.__init__(self, filename, **kw)
        self.chapter_titles = [] # To store chapter titles and their start page numbers

    def handle_pageBegin(self):
        # Override to prevent default header/footer for first few pages (title, TOC) if desired
        SimpleDocTemplate.handle_pageBegin(self)

    def afterPage(self):
        # This method is called after each page is built
        # Add footer with page number
        if self.pageTemplate.id == 'mainPages': # Only add page numbers to main content pages
            canvas = self.canv
            canvas.setFont('Helvetica', 10)
            page_num_text = f"Page {canvas.getPageNumber()}"
            canvas.drawString(letter[0] - inch - canvas.stringWidth(page_num_text, 'Helvetica', 10),
                              0.75 * inch, page_num_text)
            # You could add headers here too

# --- 3. Main PDF Generation Function ---
def create_pdf_book_advanced(output_filename, book_title, author_name, chapter_data):
    """
    Creates a PDF book with title page, TOC, chapters, and page numbers.

    Args:
        output_filename (str): The name of the output PDF file.
        book_title (str): The title of the book.
        author_name (str): The author's name.
        chapter_data (list of dict): Each dict should have 'title' and 'content'.
                                      Example: [{'title': 'Chapter 1: The Beginning', 'content': '...'}]
    """
    doc = MyDocTemplate(output_filename, pagesize=letter,
                        rightMargin=inch, leftMargin=inch,
                        topMargin=inch, bottomMargin=inch)
    styles = get_custom_styles()
    story = []

    # --- Title Page ---
    story.append(Paragraph(book_title, styles['BookTitle']))
    story.append(Paragraph(f"By {author_name}", styles['h2']))
    story.append(PageBreak())

    # --- Table of Contents Placeholder ---
    # We'll fill this in after the main content is generated to get correct page numbers
    toc_story_index = len(story) # Remember where TOC will start
    story.append(Paragraph("Table of Contents", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))
    # Placeholder for TOC entries
    toc_entries = []
    story.append(PageBreak())

    # --- Chapter Content ---
    for i, chapter in enumerate(chapter_data):
        # Record the start of the chapter for the TOC
        chapter_title_text = chapter.get('title', f"Chapter {i+1}")
        # Add a bookmark for the chapter title
        story.append(Paragraph(f'<seq id="chapter{i+1}"/>' + chapter_title_text, styles['ChapterTitle']))
        doc.chapter_titles.append({'title': chapter_title_text, 'id': f"chapter{i+1}"})

        # Add chapter content
        content_paragraphs = chapter['content'].split('\n\n') # Split by double newline for paragraphs
        for para_text in content_paragraphs:
            if para_text.strip():
                story.append(Paragraph(para_text, styles['BodyText']))
                story.append(Spacer(1, 0.1 * inch)) # Small space between paragraphs

        if i < len(chapter_data) - 1: # Don't add page break after the last chapter
            story.append(PageBreak())

    # --- Build the document once to get page numbers ---
    # This is a bit of a trick for ReportLab to know page numbers.
    # We build it once, then modify the TOC and build again.
    # For simpler cases, you can use a two-pass approach or Flowables that support TOC directly.
    # For this example, we'll just build it, get page numbers, and then manually insert.
    # A full-featured TOC generation requires a custom Flowable, which is more advanced.
    # For simplicity, let's just use page numbers directly.

    # Instead of a complex two-pass, let's use a simpler placeholder and direct page numbers
    # after the document is built (conceptually, ReportLab internally handles page numbers).
    # For an actual functioning TOC with page numbers, you'd typically use a TableOfContents Flowable.
    # Let's simulate for now:

    # A more robust TOC generation is usually done with a custom Flowable.
    # For demonstration, we'll collect info during the build and add a placeholder.

    # To get page numbers for the TOC accurately with ReportLab's SimpleDocTemplate,
    # you often need to build the document, get the page numbers (e.g., by creating bookmarks
    # and then processing the PDF or using a custom story builder that tracks page numbers),
    # then re-build the TOC. This is complex for a quick example.

    # Simpler approach: We'll create the TOC entries after the fact for this example,
    # assuming we could obtain page numbers. For now, it will just list titles.

    # Create frames for standard page layout (with margins)
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height,
                  id='mainPages')

    doc.addPageTemplates([
        doc.build_page_template([frame], id='mainPages', onPage=lambda canvas, doc: doc.afterPage())
    ])

    doc.build(story) # Build the document

    print(f"PDF '{output_filename}' created successfully!")
    print("\nNote: A fully dynamic Table of Contents with page numbers in ReportLab often requires")
    print("a more advanced approach (e.g., custom TOC Flowable or a two-pass rendering).")
    print("This example shows the structure and how to include page numbers in the footer.")

# --- Example Usage (YOU NEED TO PROVIDE THIS DATA) ---
if __name__ == "__main__":
    # --- THIS IS THE DATA YOU NEED TO EXTRACT FROM GOOGLE DOCS ---
    # For demonstration, I'm using placeholder data.
    # In a real scenario, you'd use the Google Drive API or manual extraction
    # to populate 'extracted_chapter_data'.

    # Simulated Table of Contents extraction (manual or API-driven)
    # Each dictionary represents a chapter
    extracted_chapter_data = [
        {
            'title': 'Chapter 1: The First Steps',
            'content': """
This is the content of the first chapter. It talks about the initial journey and challenges faced.
Paragraphs are separated by double newlines.

This is the second paragraph of chapter one. It provides more detail and expands on the previous point.
We need to ensure all text is properly formatted.

Another paragraph here.
"""
        },
        {
            'title': 'Chapter 2: The Middle Road',
            'content': """
Chapter two delves into the main events and character development.
It's important for the narrative to flow smoothly.

This section might introduce new characters or plot twists.
Consider how images could enhance understanding here.

More content for chapter two.
"""
        },
        {
            'title': 'Chapter 3: The Conclusion',
            'content': """
The final chapter brings everything to a close, resolving conflicts and summarizing themes.

All loose ends are tied up, and the story reaches its natural end.

Thank you for reading this book!
"""
        }
    ]

    book_title = "My Grand Adventure Book"
    author_name = "AI Assistant"
    output_pdf_name = "GrandAdventureBook.pdf"

    create_pdf_book_advanced(output_pdf_name, book_title, author_name, extracted_chapter_data)

    # Example of how you could imagine extracting data (PSEUDOCODE - NOT REAL PYTHON)
    # from google_docs_api import GoogleDocsAPI

    # api = GoogleDocsAPI(credentials_path='path/to/your/credentials.json')
    # toc_doc_id = "YOUR_TOC_DOC_ID_FROM_URL"
    # toc_content = api.get_document_content(toc_doc_id)
    # chapter_links = api.extract_links_from_toc(toc_content) # You'd write this logic

    # real_extracted_chapter_data = []
    # for link in chapter_links:
    #     chapter_doc_id = api.get_doc_id_from_link(link)
    #     chapter_text = api.get_document_content(chapter_doc_id)
    #     chapter_title = api.extract_title_from_content(chapter_text) # Or from TOC entry
    #     real_extracted_chapter_data.append({'title': chapter_title, 'content': chapter_text})

    # create_pdf_book_advanced(output_pdf_name, book_title, author_name, real_extracted_chapter_data)