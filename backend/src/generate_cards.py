import os
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBmjdUQT62OK8qQs5g_nB3jFg88ddqbEqs")  # Replace with your actual API key

# 📂 Base directory containing grade folders
BASE_PDF_DIR = "/Users/lakshiitakalyanasundaram/Desktop/Machine Learning/Flash Card generator/PDFS"

# 🎯 Function to extract text from a PDF
def extract_text_from_pdf(pdf_path, chapter_number):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            if f"Chapter {chapter_number}" in page.get_text():  # Basic filtering for chapter text
                text += page.get_text()
    return text if text else None

# 🤖 Function to generate flashcards
def generate_flashcards(text, num_cards):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"Generate {num_cards} flashcards in question-answer format. Provide each flashcard as 'Q: <question> | A: <answer>'. Do not add numbering or extra text.\n{text}"
    response = model.generate_content(prompt)

    if response and response.text:
        flashcards = [card.strip() for card in response.text.split("\n") if card.strip()]
        qa_flashcards = [card for card in flashcards if "Q:" in card and "A:" in card]
        
        return qa_flashcards[:num_cards] if qa_flashcards else ["⚠️ No flashcards could be generated!"]
    return ["⚠️ No flashcards could be generated!"]

# 🏗️ Main function to handle user input
def main():
    print("\n📚 Flashcard Generator CLI 📚\n")

    # 1️⃣ Select Grade
    grades = sorted(os.listdir(BASE_PDF_DIR))
    print("Select your grade:")
    for i, grade in enumerate(grades, 1):
        print(f"{i}. {grade}")
    
    grade_choice = int(input("Enter the number of your grade: ")) - 1
    selected_grade = grades[grade_choice]

    # 2️⃣ Select Subject
    subject_dir = os.path.join(BASE_PDF_DIR, selected_grade)
    subjects = sorted(os.listdir(subject_dir))
    print("\nSelect your subject:")
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")
    
    subject_choice = int(input("Enter the number of your subject: ")) - 1
    selected_subject = subjects[subject_choice]

    # 3️⃣ Get Chapter Number
    chapter_number = input("\nEnter the chapter number: ")

    # 4️⃣ Get Number of Flashcards
    num_cards = int(input("Enter the number of flashcards to generate: "))

    # 5️⃣ Extract Text from PDF
    pdf_path = os.path.join(subject_dir, selected_subject)
    extracted_text = extract_text_from_pdf(pdf_path, chapter_number)

    if not extracted_text:
        print("⚠️ Could not find text for the specified chapter. Please check your input.")
        return

    # 6️⃣ Generate Flashcards
    flashcards = generate_flashcards(extracted_text, num_cards)

    # 7️⃣ Display Flashcards
    print("\n🎴 Generated Flashcards:\n")
    for i, card in enumerate(flashcards, 1):
        print(f"🔹 {card}")

# 🚀 Run the script
if __name__ == "__main__":
    main()
