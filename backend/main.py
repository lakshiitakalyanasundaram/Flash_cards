from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from generate_cards import generate_flashcards
from extract_text import extract_text_from_pdf

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

BASE_PDF_DIR = os.path.abspath("PDFS")
print(f"📂 PDF Base Directory: {BASE_PDF_DIR}")

# ✅ Subject Mapping
subjects = {"1": "Biology", "2": "Chemistry", "3": "Civics", "4": "Economics", "5": "History", "6": "Maths"}

# 📌 Endpoint to get available subjects
@app.get("/subjects")
async def get_subjects():
    return {"subjects": subjects}

# 📌 `/generate_flashcards` Endpoint (uses generate_cards.py, which internally calls extract_text.py)
@app.post("/generate_flashcards")
async def generate_flashcards_route(request: FlashcardRequest):
    try:
        print(f"🔹 Received Request: {request}")

        subject_folder = subjects.get(request.subject)
        if not subject_folder:
            raise HTTPException(status_code=400, detail="Invalid subject choice!")

        print(f"📂 Mapped Subject Folder: {subject_folder}")

        # Directly call generate_flashcards (which internally calls extract_text.py)
        text = extract_text_from_pdf(request.grade, subject_folder, request.chapter)  # Extract text from PDF
        flashcards = generate_flashcards(text, request.num_flashcards)  # Pass extracted text & num_flashcards



        print(f"✅ Flashcards Generated: {flashcards}")
        return {"flashcards": flashcards}

    except Exception as e:
        print(f"❌ FastAPI Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 🏠 Home route
@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI Flashcard Generator!"}