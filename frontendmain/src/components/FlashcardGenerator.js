
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./FlashcardGenerator.css"; // External CSS for better styling

const FlashcardGenerator = () => {
    const [grade, setGrade] = useState("");
    const [subjects, setSubjects] = useState({});
    const [subject, setSubject] = useState("");
    const [chapter, setChapter] = useState("");
    const [numFlashcards, setNumFlashcards] = useState("");
    const [flashcards, setFlashcards] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [flipped, setFlipped] = useState(false);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/subjects")
            .then(response => setSubjects(response.data.subjects || {}))
            .catch(err => console.error("Error fetching subjects:", err));
    }, []);

    const handleGenerate = async () => {
        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:8000/generate_flashcards", {
                grade: grade.toString(),
                subject: subject.toString(),
                chapter: chapter.toString(),
                num_flashcards: parseInt(numFlashcards) || 1
            });
            setFlashcards(response.data.flashcards);
            setError(null);
            setCurrentIndex(0); // Reset to the first card
        } catch (error) {
            console.error("Error generating flashcards:", error);
            setError("Failed to generate flashcards. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleFlip = () => {
        setFlipped(!flipped);
    };

    const handleSwipe = (direction) => {
        setFlipped(false); // Reset flip state when changing cards
        if (direction === "left" && currentIndex < flashcards.length - 1) {
            setCurrentIndex(currentIndex + 1);
        } else if (direction === "right" && currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
        }
    };

    return (
        <div className="container">
            <h2>Flashcard Generator</h2>
            
            {/* Input Fields Container */}
            <div className="input-container">
                <input type="text" placeholder="Grade" value={grade} onChange={(e) => setGrade(e.target.value)} />
                <select value={subject} onChange={(e) => setSubject(e.target.value)}>
                    <option value="">Select Subject</option>
                    {Object.entries(subjects).map(([id, name]) => (
                        <option key={id} value={id}>{name}</option>
                    ))}
                </select>
                <input type="text" placeholder="Chapter" value={chapter} onChange={(e) => setChapter(e.target.value)} />    
                <input type="number" placeholder="Number of Flashcards" value={numFlashcards} onChange={(e) => setNumFlashcards(e.target.value)} />
                <button onClick={handleGenerate} disabled={loading}>{loading ? "Generating..." : "Generate Flashcards"}</button>
            </div>

            {error && <p className="error">{error}</p>}

            {/* Flashcard Display */}
            <div className="flashcard-stack">
                {flashcards.length > 0 && (
                    <div className={`flashcard ${flipped ? "flipped" : ""}`} onClick={handleFlip}>
                        <div className="flashcard-inner">
                            <div className="flashcard-front">
                                <p><strong>Q{currentIndex + 1}:</strong> {flashcards[currentIndex].split("|")[0].replace("Q:", "").trim()}</p>
                            </div>
                            <div className="flashcard-back">
                                <p><strong>A:</strong> {flashcards[currentIndex].split("|")[1].replace("A:", "").trim()}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Swipe Controls */}
            {flashcards && flashcards.length > 0 && (
    <div className="controls">
        <button 
            onClick={() => handleSwipe("right")} 
            disabled={currentIndex === 0} 
            className="nav-btn"
        >
            ◀
        </button>
        <button 
            onClick={() => handleSwipe("left")} 
            disabled={currentIndex === flashcards.length - 1} 
            className="nav-btn"
        >
            ▶
        </button>
    </div>
)}
        </div>
    );
};

export default FlashcardGenerator;
