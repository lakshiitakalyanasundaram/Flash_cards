import React, { useState } from "react";
import { motion } from "framer-motion";
import Flashcard from "./components/Flashcard";
import FlashcardGenerator from "./components/FlashcardGenerator";

const App = () => {
  const [flashcards, setFlashcards] = useState([]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600 p-6 text-white">
      {/* Only FlashcardGenerator will contain the form */}
      <FlashcardGenerator setFlashcards={setFlashcards} />

      {/* Display flashcards when available */}
      {flashcards.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"
        >
          {flashcards.map((card, index) => (
            <Flashcard key={index} index={index + 1} card={card} />
          ))}
        </motion.div>
      )}
    </div>
  );
};

export default App;
