import fitz  # PyMuPDF for PDF text extraction
import os

# 📂 Base directory for PDFs
BASE_PDF_DIR = "/Users/lakshiitakalyanasundaram/Desktop/Machine Learning/Flash Card generator/PDFS"

def extract_text_from_pdf(grade, subject, chapter):
    """Extracts text from a specific PDF file."""
    pdf_path = os.path.join(BASE_PDF_DIR, grade, subject, f"{chapter}.pdf")

    if not os.path.isfile(pdf_path):  # Check if the file exists
        print(f"❌ Error: File '{pdf_path}' not found.")
        return ""

    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    print(f"✅ Extracted Text (First 500 chars):\n{text[:500]}")
    return text if text.strip() else None
