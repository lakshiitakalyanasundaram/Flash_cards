import os
import fitz  # PyMuPDF for PDF text extraction
import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBmjdUQT62OK8qQs5g_nB3jFg88ddqbEqs")  # Replace with your actual API key

# 📂 Base directory containing grade folders
BASE_PDF_DIR = "/Users/lakshiitakalyanasundaram/Desktop/Machine Learning/Flash Card generator/PDFS"

# 🎯 Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# 🤖 Function to generate flashcards
def generate_flashcards(text, num_cards):
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    
    prompt = f"Generate {num_cards} flashcards in question-answer format. Provide each flashcard as 'Q: <question> | A: <answer>'. Do not add numbering or extra text.\n{text}"
    response = model.generate_content(prompt)

    if response and response.text:
        flashcards = [card.strip() for card in response.text.split("\n") if card.strip()]
        qa_flashcards = []
        
        for card in flashcards:
            if "Q:" in card and "A:" in card:
                qa_flashcards.append(card)
                if len(qa_flashcards) == num_cards:
                    break
        
        return qa_flashcards
    return ["⚠️ No flashcards could be generated!"]

# 🚀 Streamlit UI
st.title("📚 AI Flashcard Generator")

# 📌 Select Grade
grade = st.text_input("Enter your grade (e.g., 9, 10):").strip()

# ✅ Different subject lists based on grade
default_subjects = {
    "1": "Biology", "2": "Chemistry", "3": "Maths", 
    "4": "History", "5": "Civics", "6": "Economics"
}  # ❌ Removed Geography & Physics

grade_10_subjects = {}

# 📌 Fetch subjects dynamically for Grade 10
if grade:
    grade_path = os.path.join(BASE_PDF_DIR, grade)
    if os.path.exists(grade_path):
        if grade == "10":
            grade_10_subjects = grade_10_subjects = {str(i + 1): sub for i, sub in enumerate(sorted(os.listdir(grade_path))) if sub != ".DS_Store"}


# 🎯 Separate dropdowns for Grade 10 vs. Others
if grade == "10":
    subject_choice = st.selectbox("Select a subject:", list(grade_10_subjects.keys()), format_func=lambda x: grade_10_subjects[x])
    subject = grade_10_subjects[subject_choice]
else:
    subject_choice = st.selectbox("Select a subject:", list(default_subjects.keys()), format_func=lambda x: default_subjects[x])
    subject = default_subjects[subject_choice]

# 📖 Enter Chapter Number
chapter_number = st.text_input(f"Enter the chapter number for {subject} (e.g., 1):").strip()

# 🔍 Check if file exists
if grade and subject and chapter_number:
    pdf_filename = f"{chapter_number}.pdf"
    pdf_path = os.path.join(BASE_PDF_DIR, grade, subject, pdf_filename)

    print(f"Checking for file: {pdf_path}")

    if not os.path.exists(pdf_path):
        available_files = os.listdir(os.path.join(BASE_PDF_DIR, grade, subject)) if os.path.exists(os.path.join(BASE_PDF_DIR, grade, subject)) else []
        st.error(f"❌ No file found for {subject}, Grade {grade}, Chapter {chapter_number}!\n📂 Available files: {available_files}")
        st.stop()

    extracted_text = extract_text_from_pdf(pdf_path)

    # 🔢 Enter number of flashcards
    num_cards = st.number_input("Enter number of flashcards:", min_value=1, value=5, step=1)

    # 📝 Generate Flashcards
    if st.button("Generate Flashcards"):
        flashcards = generate_flashcards(extracted_text, num_cards)
        flashcards.insert(0, "Here are your flashcards based on the text in question-answer format.")
        
        st.session_state.flashcards = flashcards
        st.session_state.index = 0

# 🎴 Flashcard Navigation
if "flashcards" in st.session_state and st.session_state.flashcards:
    flashcards = st.session_state.flashcards
    index = st.session_state.index

    with st.container():
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #3a3f36; text-align: center; font-size: 18px; color: white;">
                <strong>Flashcard {index}/{len(flashcards) - 1}</strong>
                <hr>
                <p>{flashcards[index]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous") and index > 0:
            st.session_state.index -= 1

    with col3:
        if st.button("➡️ Next") and index < len(flashcards) - 1:
            st.session_state.index += 1
