import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { GameDataContext } from './App';

const GameLobbyPage = ({ games }) => {
  const { setGameData } = useContext(GameDataContext);

  const handleJoinGame = (game) => {
    console.log("handleJoinGame")
    // Replace this with the logic to set teamName and userId
    const teamName = 'team1';
    const userId = 'user1';


    // Update gameData context with the provided data
    setGameData({ game, teamName, userId });
  };

  return (
    <div>
      <h2>Game Lobby Page</h2>
      {games.map((game) => (
        <div key={game.gameId}>
          <h3>{game.gameName}</h3>
          <Link to="/game">
            <button onClick={() => handleJoinGame(game)}>Join Game</button>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default GameLobbyPage;
