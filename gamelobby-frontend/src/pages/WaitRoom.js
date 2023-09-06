import React, { useEffect, useState, useCallback } from 'react';

import { useLocation } from 'react-router-dom';

const WaitRoom = () => {
  // Use the useLocation hook to access the state data passed from the GameLobby
  const location = useLocation();
  const {
    game_id,
    category,
    difficulty,
    start_time,
    status,
    user_id,
    team_name,
    participant_count,
    users_joined,
  } = location.state;

  // Calculate the remaining time as a difference between the start_time and the current time
  const calculateRemainingTime = useCallback(() => {
    const startTimeMillis = new Date(start_time).getTime();
    const currentTimeMillis = new Date().getTime();
    return startTimeMillis - currentTimeMillis;
  }, [start_time]);

  // State to hold the remaining time
  const [remainingTime, setRemainingTime] = useState(calculateRemainingTime());

  // Update the remaining time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setRemainingTime(calculateRemainingTime());
    }, 1000);

    // Clean up the interval when the component is unmounted
    return () => clearInterval(timer);
  }, [calculateRemainingTime]);

  // Format the remaining time as minutes and seconds
  const minutes = Math.floor(remainingTime / 1000 / 60);
  const seconds = Math.floor((remainingTime / 1000) % 60);

  return (
    <div className="container">
      <h1>Waiting Room</h1>

      {/* Display Game Details */}
      <div>
        <h2>Game Details</h2>
        <p>Game ID: {game_id}</p>
        <p>Category: {category}</p>
        <p>Difficulty: {difficulty}</p>
        <p>Start Time: {start_time}</p>
        <p>Status: {status}</p>
        <p>Remaining Time: {remainingTime > 0 ? (
          <p>{minutes} minutes {seconds} seconds</p>
        ) : (
          <p>The game has started!</p>
        )}</p>
        <p>Number of Participants: {participant_count}</p>
        {/* Add other game details as needed */}
      </div>

      {/* Display Team Members */}
      <div>
        <h2>Team Members</h2>
        <p>Team Name: {team_name}</p>
        {users_joined && users_joined.length > 0 ? (
          <ul>
            {users_joined.map((member, index) => (
              <li key={index}>{member}</li>
            ))}
          </ul>
        ) : (
          <p>No team members joined yet.</p>
        )}
      </div>
    </div>
  );
};

export default WaitRoom;
