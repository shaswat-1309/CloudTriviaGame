import React from 'react';

const GameCard = ({ game }) => {
  return (
    <div>
      <p>Difficulty: {game.difficulty}</p>
      <p>Category: {game.category}</p>
      {/* Render other game details */}
    </div>
  );
};

export default GameCard;
