import fitz  # PyMuPDF
import pytesseract
from docx import Document
from PIL import Image

# Step 1: Extract pages from PDF
pdf_file = 'bio.pdf'
doc = fitz.open(pdf_file)

# Step 2: For each page, extract images for OCR
for page_num in range(len(doc)):
    print(page_num)
    page = doc.load_page(page_num)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Step 3: Perform OCR on the image
    text = pytesseract.image_to_string(img, lang='eng')
    # Optional: Extract font information if available

    # Step 4: Create or append to DOCX
    document = Document()
    document.add_paragraph(text)
    # Apply font styles if identified
    document.save('output.docx')
