import React, { createContext, useState } from 'react';
import { BrowserRouter as Router, Link, Route, Routes } from 'react-router-dom';
import GameLobbyPage from './GameLobbyPage';
import Game from './Game';

// Create a React Context for storing game data
export const GameDataContext = createContext();

const App = () => {
  // State to hold game data
  const [gameData, setGameData] = useState({
    game : {
      gameId: '7ff55795f-2d43-46de-b973-ba27167158ae', gameName: 'Game 1', category: "Sports", difficulty: "Medium"
    },
    teamName: 'team1',
    userId: 'user1',
  });

  // Dummy game data, replace this with your actual game data
  const games = [
    { gameId: 'ff55795f-2d43-46de-b973-ba27167158ae', gameName: 'Game 1', category: "Sports", difficulty: "Medium" },
    { gameId: 'game2', gameName: 'Game 2', category: "Science", difficulty: "Difficult" },
    { gameId: 'game3', gameName: 'Game 3', category: "Misc", difficulty: "Easy" },
  ];

  return (
    <Router>
      <div>
        <h1>Trivia game!</h1>

        {/* Define routes */}
        <Routes>
          <Route
            path="/"
            element={
              <GameDataContext.Provider value={{ gameData, setGameData }}>
                <GameLobbyPage games={games} />
              </GameDataContext.Provider>
            }
          />
          <Route
            path="/game"
            element={
              <GameDataContext.Provider value={{ gameData, setGameData }}>
                <Game />
              </GameDataContext.Provider>
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
