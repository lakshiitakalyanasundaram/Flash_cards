let backendUrl;

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    backendUrl = "http://127.0.0.1:5000/generate_flashcards"; // For local access
} else {
    backendUrl = "http://10.3.154.18:5000/generate_flashcards"; // For network access
}

console.log("Backend URL:", backendUrl);


document.getElementById("generate-btn").addEventListener("click", generateFlashcards);

function generateFlashcards() {
    const grade = document.getElementById("grade").value;
    const subject = document.getElementById("subject").value;
    const chapterNumber = document.getElementById("chapter").value;
    const numCards = document.getElementById("num-cards").value;

    const data = {
        grade: grade,
        subject: subject,
        chapter_number: chapterNumber,
        num_cards: numCards
    };

    fetch(backendUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.flashcards) {
            displayFlashcards(result.flashcards);
        } else {
            alert(result.error || "An error occurred while generating flashcards.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to fetch flashcards.");
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
