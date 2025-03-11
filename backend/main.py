from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBmjdUQT62OK8qQs5g_nB3jFg88ddqbEqs")

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define the request model once
class FlashcardRequest(BaseModel):
    grade: str
    subject: str
    chapter: str
    num_flashcards: int  # Must be an integer

# 📂 Base directory containing PDFs
BASE_PDF_DIR = "PDFS"

# ✅ Subject Mapping
subjects = {"1": "Biology", "2": "Chemistry", "3": "Civics", "4": "Economics", "5": "History", "6": "Maths"}

# 🎯 Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

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

# 📌 Endpoint to get available subjects
@app.get("/subjects")
async def get_subjects():
    return {"subjects": subjects}

# 📌 Correct `/generate_flashcards` Endpoint
@app.post("/generate_flashcards")
async def generate_flashcards_route(request: FlashcardRequest):
    try:
        print(f"🔹 Received subject ID: {request.subject}")  # Debugging
        subject_folder = subjects.get(request.subject)

        if not subject_folder:
            raise HTTPException(status_code=400, detail="Invalid subject choice!")

        print(f"📂 Mapped to subject folder: {subject_folder}")  # Debugging

        # Construct the PDF path
        pdf_path = os.path.join(BASE_PDF_DIR, request.grade, subject_folder, f"{request.chapter}.pdf")
        print(f"📄 Checking PDF path: {pdf_path}")

        # Check if the file exists
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"File '{pdf_path}' not found.")

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Generate flashcards
        flashcards = generate_flashcards(extracted_text, request.num_flashcards)

        return {"flashcards": flashcards}

    except Exception as e:
        print(f"❌ Error: {e}")  # Debugging
        raise HTTPException(status_code=500, detail=str(e))

# 🏠 Home route
@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI Flashcard Generator!"}
