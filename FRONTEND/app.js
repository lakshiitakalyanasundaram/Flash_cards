const API_KEY = "6397b0ee5e7d0c5b9b10547b6d75ea1bae5b4e8a982354ab369c5c4613654d07";

let backendUrl;

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    backendUrl = "http://127.0.0.1:5000/generate_flashcards"; // For local access
} else {
    backendUrl = "http://10.3.154.18:5000/generate_flashcards"; // For network access
}

console.log("Backend URL:", backendUrl);


document.getElementById("generate-btn").addEventListener("click", generateFlashcards);

function generateFlashcards() {
    document.getElementById("generate-btn").addEventListener("click", function() {
        const grade = document.getElementById("grade").value;
        const subject = document.getElementById("subject").value;
        const chapter_number = document.getElementById("chapter").value;
    
        fetch("http://127.0.0.1:5000/generate_flashcards", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                grade: parseInt(grade),
                subject: parseInt(subject),
                chapter_number: parseInt(chapter_number)
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ API Response:", data);
            document.getElementById("flashcard-container").innerText = JSON.stringify(data);
        })
        .catch(error => console.error("❌ Error:", error));
    });
    
}

function displayFlashcards(flashcards) {
    const flashcardContainer = document.getElementById("flashcard");
    flashcardContainer.innerHTML = "";

    flashcards.forEach((flashcard, index) => {
        const flashcardElement = document.createElement("div");
        flashcardElement.classList.add("flashcard-item");
        
        flashcardElement.innerHTML = `
            <div class="flashcard-front">
                <h3>Flashcard ${index + 1}</h3>
                <p>${flashcard.question}</p>
            </div>
            <div class="flashcard-back">
                <p>${flashcard.answer}</p>
            </div>
        `;
        
        flashcardContainer.appendChild(flashcardElement);
    });
}
