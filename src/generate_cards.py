import os
import fitz  # PyMuPDF for PDF text extraction
import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyB2rIWI3_fvZe1OxHmlc7Bqf2_l_zJ0fpY")  # Replace with your actual key

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
grade = st.text_input("Enter your grade (e.g., 9):").strip()

# 🧪 Select Subject
subjects = {"1": "Biology", "2": "Chemistry"}
subject_choice = st.selectbox("Select a subject:", list(subjects.keys()), format_func=lambda x: subjects[x])
subject = subjects[subject_choice]

# 📖 Enter Chapter Number
chapter_number = st.text_input(f"Enter the chapter number for {subject} (e.g., 1):").strip()

# 🔍 Check if file exists
if grade and subject and chapter_number:
    pdf_filename = f"{chapter_number}.pdf"
    pdf_path = os.path.join(BASE_PDF_DIR, grade, subject, pdf_filename)

    # 🔥 Debugging: Print available files
    if not os.path.exists(pdf_path):
        available_files = os.listdir(os.path.join(BASE_PDF_DIR, grade, subject)) if os.path.exists(os.path.join(BASE_PDF_DIR, grade, subject)) else []
        st.error(f"❌ No file found for {subject}, Grade {grade}, Chapter {chapter_number}!\nAvailable files: {available_files}")
        st.stop()

    # 📂 Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)

    # 🔢 Enter number of flashcards
    num_cards = st.number_input("Enter number of flashcards:", min_value=1, value=5, step=1)

    # 📝 Generate Flashcards
    if st.button("Generate Flashcards"):
        flashcards = generate_flashcards(extracted_text, num_cards)
        
        # Include intro message as the first card
        flashcards.insert(0, "Here are your flashcards based on the text in question-answer format.")
        
        st.session_state.flashcards = flashcards
        st.session_state.index = 0

# 🎴 Flashcard Navigation
if "flashcards" in st.session_state and st.session_state.flashcards:
    flashcards = st.session_state.flashcards
    index = st.session_state.index

    # 📌 Show Current Flashcard in a Bigger Box
    with st.container():
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #4CAF50; border-radius: 10px; background-color: ##3a3f36; text-align: center; font-size: 18px;">
                <strong>Flashcard {index}/{len(flashcards) - 1}</strong>
                <hr>
                <p>{flashcards[index]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # ⬅️ ➡️ Navigation Buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous") and index > 0:
            st.session_state.index -= 1

    with col3:
        if st.button("➡️ Next") and index < len(flashcards) - 1:
            st.session_state.index += 1
