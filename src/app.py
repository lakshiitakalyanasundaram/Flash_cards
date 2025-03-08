from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
import traceback 

FLASHCARD_API_KEY = "6397b0ee5e7d0c5b9b10547b6d75ea1bae5b4e8a982354ab369c5c4613654d07"
# Configure Gemini API
api_key = "AIzaSyB2rIWI3_fvZe1OxHmlc7Bqf2_l_zJ0fpY"  # Replace with your actual key
genai.configure(api_key=api_key)

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to generate flashcards using LLM (Google Generative AI)
def generate_flashcards(text):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Generate flashcards in question-answer format from the following text:\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Route to generate flashcards
@app.route('/generate_flashcards', methods=['POST'])
def generate_flashcards_route():
    try:
        data = request.get_json()
        
        print("🔹 Received Data:", data)  # Debugging print
        
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        
        grade = data.get('grade')
        subject = data.get('subject')
        chapter_number = data.get('chapter_number')

        if not grade or not subject or not chapter_number:
            return jsonify({"error": "Missing required fields (grade, subject, chapter_number)"}), 400

        # Map subjects to folder names
        subjects = {"1": "Biology", "2": "Chemistry"}
        subject_folder = subjects.get(subject, None)

        if not subject_folder:
            return jsonify({"error": "Invalid subject choice!"}), 400

        # Construct the PDF path
        pdf_path = os.path.join("PDFS", grade, subject_folder, f"{chapter_number}.pdf")
        
        # Check if the file exists
        if not os.path.exists(pdf_path):
            return jsonify({"error": f"File '{pdf_path}' not found."}), 400

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Generate flashcards using LLM
        flashcards = generate_flashcards(extracted_text)

        # Return the flashcards
        return jsonify({"flashcards": flashcards})

    except Exception as e:
        print("❌ ERROR:", str(e))
        print(traceback.format_exc())  # Print full error details
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
# Home route
@app.route('/')
def home():
    return "Welcome to the Flashcard Generator API!"

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 
