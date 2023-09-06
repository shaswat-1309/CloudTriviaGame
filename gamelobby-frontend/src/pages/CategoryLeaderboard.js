import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const CategoryLeaderboard = () => {

  // State to store category leaderboard data, selected category, selected time frame, and categories list
  const [categoryLeaderboard, setCategoryLeaderboard] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedTimeFrame, setSelectedTimeFrame] = useState('all time');
  const [categories, setCategories] = useState([]);

  // Effect to fetch category leaderboard data when selected category or time frame changes
  useEffect(() => {
    fetchCategoryLeaderboard();
  }, [selectedCategory, selectedTimeFrame]);

  // Function to fetch category leaderboard data from API
  const fetchCategoryLeaderboard = () => {
    // API endpoint for fetching the team leaderboard and categories list
    fetch(`https://b1gzkxcubi.execute-api.us-east-1.amazonaws.com/Prod/category_leaderboard?category=${encodeURIComponent(selectedCategory)}&time_frame=${encodeURIComponent(selectedTimeFrame)}`)
      .then(response => response.json())
      .then(data => {
        setCategoryLeaderboard(data.leaderboard);
        setCategories(data.categories);
      })
      .catch(error => console.error('Error fetching category leaderboard data:', error));
  };

  // Event handlers for category filter
  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
  };

  // Event handlers for time frame filter
  const handleTimeFrameChange = (event) => {
    setSelectedTimeFrame(event.target.value);
  };

  // Function to render the leaderboard table
  const renderLeaderboardTable = () => {
    return (
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Team Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {categoryLeaderboard.map(entry => (
            <tr key={entry.team_name}>
              <td>{entry.team_name}</td>
              <td>{entry.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Team Leaderboard</h1>
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
        {categoryLeaderboard.length > 0 ? (
          renderLeaderboardTable()
        ) : (
          <p>No data available for the selected category and time frame.</p>
        )}
      </div>
      {/* Button to go to the visualization page */}
      <Link to="/visualize">
        <button className="btn btn-primary mr-2">Visualize</button>
      </Link>
      {/* Button to go back to the leaderboard */}
      <Link to="/leaderboard">
        <button className="btn btn-primary">Go back to Leaderboard</button>
      </Link>
    </div>
  );
};

export default CategoryLeaderboard;
