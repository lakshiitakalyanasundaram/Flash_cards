import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import Flashcard from "./Flashcard";


const App = () => {
  const [grade, setGrade] = useState("");
  const [subject, setSubject] = useState("1");
  const [chapter, setChapter] = useState("");
  const [numCards, setNumCards] = useState(5);
  const [flashcards, setFlashcards] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
  setLoading(true);
  try {
    const requestData = {
      grade: grade.toString(),
      subject: subject.toString(),
      chapter: chapter.toString(),
      num_flashcards: Number(numCards)
      };
    

    console.log("📤 Sending request:", requestData);  // Debugging

    const response = await axios.post(
      "http://127.0.0.1:8000/generate_flashcards",
      requestData,
      { headers: { "Content-Type": "application/json" } }  // Ensure JSON format
    );

    console.log("✅ API Response:", response.data);
    setFlashcards(response.data);
  } catch (error) {
    console.error("❌ Error generating flashcards:", error.response ? error.response.data : error);
  }
  setLoading(false);
};

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 p-6 text-white">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white p-6 rounded-lg shadow-xl text-black w-full max-w-lg"
      >
        <h1 className="text-2xl font-bold text-center mb-4">📚 Flashcard Generator</h1>
        <div className="mb-4">
          <label className="block mb-1">Grade:</label>
          <input
            type="text"
            value={grade}
            onChange={(e) => setGrade(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Subject:</label>
          <select
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="1">Biology</option>
            <option value="2">Chemistry</option>
            <option value="3">Civics</option>
            <option value="4">Economics</option>
            <option value="5">History</option>
            <option value="6">Maths</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block mb-1">Chapter Number:</label>
          <input
            type="text"
            value={chapter}
            onChange={(e) => setChapter(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Number of Flashcards:</label>
          <input
            type="number"
            value={numCards}
            onChange={(e) => setNumCards(Number(e.target.value))}
            className="w-full p-2 border rounded"
          />
        </div>
        <button
          onClick={handleGenerate}
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Flashcards"}
        </button>
      </motion.div>

      {flashcards.length > 0 && (
        <div className="mt-8">
          {flashcards.map((card, index) => (
            <Flashcard key={index} index={index + 1} card={card} />
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
