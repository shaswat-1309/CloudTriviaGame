import React from 'react';
import { Link } from 'react-router-dom';

const Leaderboard = () => {
  return (
    <div className="container mt-5 text-center">
      <h1>Welcome to the Leaderboard</h1>
      <div className="d-grid gap-3 col-6 mx-auto mt-5">
        {/* Link to the Team Leaderboard */}
        <Link to="/team_leaderboard">
          <button className="btn btn-primary btn-lg">Team Leaderboard</button>
        </Link>
        {/* Link to the Player Leaderboard */}
        <Link to="/player_leaderboard">
          <button className="btn btn-secondary btn-lg">Player Leaderboard</button>
        </Link>
      </div>
    </div>
  );
};

export default Leaderboard;
