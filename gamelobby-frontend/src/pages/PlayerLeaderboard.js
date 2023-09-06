import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const PlayerLeaderboard = () => {

  // State variables to manage player leaderboard data and filters
  const [playerLeaderboard, setPlayerLeaderboard] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedTimeFrame, setSelectedTimeFrame] = useState('all time');
  const [categories, setCategories] = useState([]);

  // Effect to fetch player leaderboard data when filters change
  useEffect(() => {
    fetchPlayerLeaderboard();
  }, [selectedCategory, selectedTimeFrame]);

  // Function to fetch player leaderboard data
  const fetchPlayerLeaderboard = () => {
    //API endpoint for fetching the player leaderboard and categories list
    fetch(`https://b1gzkxcubi.execute-api.us-east-1.amazonaws.com/Prod/players_leaderboard?category=${encodeURIComponent(selectedCategory)}&time_frame=${encodeURIComponent(selectedTimeFrame)}`)
      .then(response => response.json())
      .then(data => {
        setPlayerLeaderboard(data.leaderboard);
        setCategories(data.categories);
      })
      .catch(error => console.error('Error fetching player leaderboard data:', error));
  };

  // Event handlers for filter changes
  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
  };

  const handleTimeFrameChange = (event) => {
    setSelectedTimeFrame(event.target.value);
  };

  // Function to render the player leaderboard table
  const renderLeaderboardTable = () => {
    return (
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Player ID</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {playerLeaderboard.map(entry => (
            <tr key={entry.playerId}>
              <td>{entry.playerId}</td>
              <td>{entry.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Player Leaderboard</h1>
      <div className="row mb-3">
        <div className="col-md-4">
          <label htmlFor="categorySelect">Select Category:</label>
          <select className="form-select" id="categorySelect" value={selectedCategory} onChange={handleCategoryChange}>
            <option value="">-- Select a category --</option>
            {categories.map(category => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>
        <div className="col-md-4">
          <label htmlFor="timeFrameSelect">Select Time Frame:</label>
          <select className="form-select" id="timeFrameSelect" value={selectedTimeFrame} onChange={handleTimeFrameChange}>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="all time">All Time</option>
          </select>
        </div>
      </div>

      <div>
        {/* Display the leaderboard table if data is available */}
        {playerLeaderboard.length > 0 ? (
          renderLeaderboardTable()
        ) : (
          <div>Loading...</div>
        )}
      </div>

      {/* Button to go back to the leaderboard */}
      <Link to="/leaderboard">
        <button className="btn btn-primary">Go Back to Leaderboard</button>
      </Link>
    </div>
  );
};

export default PlayerLeaderboard;
