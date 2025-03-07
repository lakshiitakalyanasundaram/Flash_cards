import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBLbit4NN5_kQGE5ykQrVb8rUi1fdzrMBQ")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    print(f"Extracted Text (First 500 chars): {text[:500]}")  # Debug: print first 500 chars of extracted text
    return text

def generate_flashcards(text):
    model = model="gemini-1.5"

    prompt = f"Generate flashcards in question-answer format from the following text:\n{text}"
    response = model.generate_content(prompt)
    print(f"Generated Flashcards Response: {response.text[:500]}")  # Debug: print first 500 chars of the response
    return response.text

def main():
    pdf_path = "/Users/lakshiitakalyanasundaram/Desktop/Machine Learning/Flash Card generator/PDFS"  # Replace with your PDF file
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if not extracted_text:
        print("❌ No text extracted from the PDF!")
        return
    
    flashcards = generate_flashcards(extracted_text)
    if flashcards:
        print("Generated Flashcards:\n", flashcards)
    else:
        print("❌ Failed to generate flashcards.")

if __name__ == "__main__":
    main()
