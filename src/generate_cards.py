import os
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBLbit4NN5_kQGE5ykQrVb8rUi1fdzrMBQY")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_flashcards(text):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Generate flashcards in question-answer format from the following text:\n{text}"
    response = model.generate_content(prompt)
    return response.text

def main():
    # Base directory containing grade folders
    base_pdf_dir = "/Users/lakshiitakalyanasundaram/Desktop/Machine Learning/Flash Card generator/PDFS"
    
    # Check if the directory exists
    if not os.path.exists(base_pdf_dir):
        print(f"❌ Error: The folder '{base_pdf_dir}' does not exist.")
        return

    # Ask user to enter the grade number
    grade = input("Enter the grade number (e.g., 9): ").strip()
    
    # Check if the entered grade folder exists
    grade_dir = os.path.join(base_pdf_dir, grade)
    if not os.path.exists(grade_dir):
        print(f"❌ No PDF files found for Grade {grade}.")
        return

    # Ask for the subject (hardcoded for now as Biology and Chemistry)
    subjects = {"1": "Biology", "2": "Chemistry"}
    print("\nSelect a subject:")
    for num, name in subjects.items():
        print(f"{num}. {name}")
    
    subject_choice = input("\nEnter the subject number: ").strip()
    subject_folder = subjects.get(subject_choice, None)
    
    if not subject_folder:
        print("❌ Invalid subject choice!")
        return
    
    subject_dir = os.path.join(grade_dir, subject_folder)

    # Check if subject folder exists
    if not os.path.exists(subject_dir):
        print(f"❌ Error: The subject folder '{subject_folder}' does not exist for Grade {grade}.")
        return
    
    # List all PDFs (chapters) in the selected subject folder
    pdf_files = [f for f in os.listdir(subject_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ No PDF files found for Grade {grade} in {subject_folder}.")
        return

    # Ask user to enter the chapter number directly
    chapter_number = input(f"\nEnter the chapter number for {subject_folder} in Grade {grade}: ").strip()

    # Construct the PDF path based on the chapter number entered by the student
    pdf_filename = f"{chapter_number}.pdf"
    pdf_path = os.path.join(subject_dir, pdf_filename)

    # Check if the chapter file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Chapter {chapter_number} not found.")
        return

    # Extract text from the selected PDF
    print(f"\n📂 Extracting text from {pdf_filename}...")
    extracted_text = extract_text_from_pdf(pdf_path)

    # Generate flashcards from the extracted text
    print("\n📝 Generating flashcards...")
    flashcards = generate_flashcards(extracted_text)
    print("Generated Flashcards:\n", flashcards)

if __name__ == "__main__":
    main()
