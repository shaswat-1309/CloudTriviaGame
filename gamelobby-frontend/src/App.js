import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GameLobby from './pages/GameLobby';
import WaitRoom from './pages/WaitRoom';
import CategoryLeaderboard from './pages/CategoryLeaderboard';
import PlayerLeaderboard from './pages/PlayerLeaderboard';
import Leaderboard from './pages/Leaderboard';
import Visualize from './pages/Visualize';

import 'bootstrap/dist/css/bootstrap.min.css';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';



const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/gamelobby" element={<GameLobby />} />
          <Route path="/waitroom" element={<WaitRoom />}></Route>
          <Route path="/team_leaderboard" element={<CategoryLeaderboard />}></Route>
          <Route path="/player_leaderboard" element={<PlayerLeaderboard />}></Route>
          <Route path="/leaderboard" element={<Leaderboard />}></Route>
          <Route path="/visualize" element={<Visualize />}></Route>
        </Routes>
      </div>
    </Router>
  );
};

export default App;
