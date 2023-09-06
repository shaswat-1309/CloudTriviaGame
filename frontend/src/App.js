import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Admin from './admin';
import CreateGame from './Components/create_game';
import ShowGames from './Components/showgames';
import ShowQuestions from './Components/showquestions';
import AddQuestion from './Components/addquestion';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Admin />} />
        <Route path="/create_game" element={<CreateGame />} />
        <Route path="/showgames" element={<ShowGames />} />
        <Route path="/showquestions" element={<ShowQuestions />} />
        <Route path="/addquestion" element={<AddQuestion />} />
      </Routes>
    </Router>
  );
}

export default App;
