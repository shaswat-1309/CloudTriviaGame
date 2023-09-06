import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './GameLobby.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';


const GameLobby = () => {

    // State to store games, filters, and carousel index
    const [games, setGames] = useState([]);
    const [categoryFilter, setCategoryFilter] = useState('');
    const [timeframeFilter, setTimeframeFilter] = useState('');
    const [carouselIndex, setCarouselIndex] = useState(0);
    const [difficultyFilter, setDifficultyFilter] = useState('');

    // Effect to fetch games from the backend on component mount
    useEffect(() => {
        fetchGames();
    }, []);

    // Hook for navigation
    const navigate = useNavigate();

    // Function to fetch games from the backend
    const fetchGames = async () => {
        try {
            // API to fetch games from the backend
            const response = await fetch('https://b1gzkxcubi.execute-api.us-east-1.amazonaws.com/Prod/gamelobby', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                  user_id: localStorage.getItem('userid'),
                  team_name: localStorage.getItem('team'),
                }),
              });
        

            const responseBody = await response.text();

            const parsedResponse = JSON.parse(responseBody);

            setGames(parsedResponse);
        } catch (error) {
            console.error(error);
        }
    };

    // Function to calculate time remaining until game start
    const calculateTimeRemaining = (startTime) => {
        const now = new Date().getTime();
        const start = new Date(startTime).getTime();
        const diff = start - now;

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        return {
            days,
            hours,
            minutes,
            seconds,
        };
    };

    // category filter handler
    const handleCategoryFilterChange = (event) => {
        setCategoryFilter(event.target.value);
    };

    // Time frame filter handler
    const handleTimeframeFilterChange = (event) => {
        setTimeframeFilter(event.target.value);
    };

    // Handler for carousels
    const handleCarouselPrev = () => {
        setCarouselIndex((prevIndex) => prevIndex - 1);
    };

    const handleCarouselNext = () => {
        setCarouselIndex((prevIndex) => prevIndex + 1);
    };

    // Handler for difficulty filter 
    const handleDifficultyFilterChange = (event) => {
        setDifficultyFilter(event.target.value);
    };

    // Function to handle joining a game
    const handleJoinGame = async (game_id, team_name) => {
        try {
            // API to join the game
            const response = await fetch('https://b1gzkxcubi.execute-api.us-east-1.amazonaws.com/Prod/joingame', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: localStorage.getItem('userid'), 
                    team_name: localStorage.getItem('team'),
                    game_id
                }),
            });

            const responseData = await response.json();
            
            console.log(responseData)
            navigate('/waitroom', {
                state: responseData, // Pass the response data to the waiting room 
            });

        } catch (error) {
            console.error(error);
        }
    };

    // Filter and render games
    const filteredGames = games.filter((game) => {
        // Apply category filter
        if (categoryFilter && game.category !== categoryFilter) {
            return false;
        }

        // Apply timeframe filter
        const timeRemaining = calculateTimeRemaining(game.start_time);
        if (timeframeFilter === '1hour' && timeRemaining.hours >= 1) {
            return false;
        } else if (timeframeFilter === '6hours' && timeRemaining.hours >= 6) {
            return false;
        } else if (timeframeFilter === '1day' && timeRemaining.days >= 1) {
            return false;
        } else if (timeframeFilter === 'morethan1day' && timeRemaining.days < 1) {
            return false;
        }

        // Apply difficulty filter
        if (difficultyFilter && game.difficulty !== difficultyFilter) {
            return false;
        }

        return true;
    });

    return (
        <div className="container">
            <h1>Game Lobby</h1>

            <div className="filters">

                <label htmlFor="category-filter">Category:</label>
                <select id="category-filter" value={categoryFilter} onChange={handleCategoryFilterChange}>
                    <option value="">All</option>
                    <option value="science">science</option>
                    <option value="math">math</option>
                </select>

                <label htmlFor="timeframe-filter">Timeframe:</label>
                <select id="timeframe-filter" value={timeframeFilter} onChange={handleTimeframeFilterChange}>
                    <option value="">All</option>
                    <option value="1hour">Within 1 hour</option>
                    <option value="6hours">Within 6 hours</option>
                    <option value="1day">Within 1 day</option>
                    <option value="morethan1day">More than 1 day</option>
                </select>

                <label htmlFor="difficulty-filter">Difficulty:</label>
                <select id="difficulty-filter" value={difficultyFilter} onChange={handleDifficultyFilterChange}>
                    <option value="">All</option>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                </select>

            </div>

            <div className="card-carousel">
                {carouselIndex > 0 && (
                    <button className="carousel-arrow left-arrow" onClick={handleCarouselPrev}>
                        <FontAwesomeIcon icon={faChevronLeft} />
                    </button>
                )}

                {filteredGames.slice(carouselIndex, carouselIndex + 4).map((game) => {
                    const timeRemaining = calculateTimeRemaining(game.start_time);
                    return (
                        <div key={game.game_id} className="card">
                            <div className="card-header">
                                <h5 className="card-title">{game.game_id}</h5>
                            </div>
                            <div className="card-body">
                                <p className="card-text">Difficulty: {game.difficulty}</p>
                                <p className="card-text">Category: {game.category}</p>
                                <p className="card-text">Start Time: {game.start_time}</p>
                                <p className="card-text">Status: {game.status}</p>
                                <div className="timer">
                                    {`${timeRemaining.days}d ${timeRemaining.hours}h ${timeRemaining.minutes}m ${timeRemaining.seconds}s`} until the game starts!
                                </div>
                                <button className="btn btn-primary" onClick={() => handleJoinGame(game.game_id)}>Join Game</button>
                            </div>
                        </div>
                    );
                })}

                {carouselIndex < filteredGames.length - 3 && (
                    <button className="carousel-arrow right-arrow" onClick={handleCarouselNext}>
                        <FontAwesomeIcon icon={faChevronRight} />
                    </button>
                )}
            </div>
        </div>
    );
};

export default GameLobby;