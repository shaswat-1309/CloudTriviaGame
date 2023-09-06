import React, { useEffect, useState } from 'react';
import { Box, Collapse, Text, Button, Flex, Input, Select } from '@chakra-ui/react';
import { AiOutlineDown, AiOutlineUp, AiOutlineEdit, AiOutlineDelete } from 'react-icons/ai';
import axios from 'axios';
import '../App.css';
import { Link } from 'react-router-dom';

function ShowGames() {
  const [games, setGames] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [gamesPerPage] = useState(2);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await axios.get('https://aoj4yqnla8.execute-api.us-east-1.amazonaws.com/myJwtStage/show_games');
        setGames(response.data.games || []);
      } catch (error) {
        console.error(error);
      }
      finally {
        setLoading(false); // Set loading state to false after API call is completed
      }
    };

    fetchGames();
  }, []);

  const [showDetails, setShowDetails] = useState({});
  const [editableGames, setEditableGames] = useState({});

  const toggleDetails = (gameId) => {
    setShowDetails((prevState) => ({
      ...prevState,
      [gameId]: !prevState[gameId]
    }));
  };

  const toggleEditGame = (gameId) => {
    setEditableGames((prevState) => ({
      ...prevState,
      [gameId]: !prevState[gameId]
    }));
  };

  const handleEditGame = async (gameId) => {
    try {
      const updatedGame = editableGames[gameId];
      // Make API call to edit game
      const response = await axios.post('https://aoj4yqnla8.execute-api.us-east-1.amazonaws.com/myJwtStage/edit_game', {
        game_id: gameId,
        ...updatedGame // Include all fields in the request
      });
      console.log(response.data); // Handle the response as needed
      // Refresh games list
      const gamesResponse = await axios.get('https://aoj4yqnla8.execute-api.us-east-1.amazonaws.com/myJwtStage/show_games');
      setGames(gamesResponse.data.games || []);
      toggleEditGame(gameId); // Disable editing mode after updating the game
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteGame = async (gameId) => {
    try {
      // Make API call to delete game
      const response = await axios.post(' https://aoj4yqnla8.execute-api.us-east-1.amazonaws.com/myJwtStage/delete_game', { game_id: gameId });
      console.log(response.data); // Handle the response as needed
      // Refresh games list
      const gamesResponse = await axios.get('https://aoj4yqnla8.execute-api.us-east-1.amazonaws.com/myJwtStage/show_games');
      setGames(gamesResponse.data.games || []);
    } catch (error) {
      console.error(error);
    }
  };

  const handleInputChange = (e, gameId) => {
    const { name, value } = e.target;
    setEditableGames((prevState) => ({
      ...prevState,
      [gameId]: {
        ...prevState[gameId],
        [name]: value
      }
    }));
  };

  const indexOfLastGame = currentPage * gamesPerPage;
  const indexOfFirstGame = indexOfLastGame - gamesPerPage;
  const currentGames = games.slice(indexOfFirstGame, indexOfLastGame);

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };
  return (
    <Box className="containerStyles">
      <Box className="navbarStyles">
        <Link to="/" className="backButtonStyles">
          Back
        </Link>
        <Text as="h1" className="logoStyles">
          Games List
        </Text>
      </Box>
      <Box className="gamesListStyles">
        {
          loading ? (
              <>
                <Text as="h3" className="logoStyles1">
                  Loading...
                </Text>
                {/* Add your loading symbol here */}
              </>
            ) : games.length === 0 ? (
              <>
                <Text as="h3" className="logoStyles1">
                  No questions created
                </Text>
                <Button
                  as={Link}
                  to="/create_game"
                  colorScheme="teal"
                  size="sm"
                  variant="outline"
                  className="ButtonStyles2"
                >
                  Create Game
                </Button>
              </>
            ) : (
              currentGames.map((game, index) => (
          <Box key={game.game_id} className="gameItemStyles">
            <Box display="flex" alignItems="center" className="gameHeaderStyles">
              <Text as="h2" className="gameNameStyles">
                {index + 1 + (currentPage - 1) * gamesPerPage}.{' '}
                {!editableGames[game.game_id] ? (
                  game.game_name
                ) : (
                  <Input className="gameDetailStyles"
                         name="game_name"
                         value={editableGames[game.game_id]?.game_name || game.game_name}
                         onChange={(e) => handleInputChange(e, game.game_id)}
                         placeholder="Game Name"
                  />
                )}
              </Text>
              {showDetails[game.game_id] ? (
                <AiOutlineUp onClick={() => toggleDetails(game.game_id)} className="chevronIconStyles" />
              ) : (
                <AiOutlineDown onClick={() => toggleDetails(game.game_id)} className="chevronIconStyles" />
              )}
            </Box>
            <Collapse in={showDetails[game.game_id]} animateOpacity>
              <Box mt={2} className="gameDetailsStyles">
                {!editableGames[game.game_id] ? (
                  <>
                    <Text className="gameDetailStyles">Category: {game.category}</Text>
                    <Text className="gameDetailStyles">Difficulty: {game.difficulty}</Text>
                    <Text className="gameDetailStyles">No. of Questions: {game.no_of_questions}</Text>
                    <Text className="gameDetailStyles">Start Time: {game.start_time}</Text>
                  </>
                ) : (
                  <>
                    <Input className="gameDetailStyles"
                           name="category"
                           value={editableGames[game.game_id]?.category || game.category}
                           onChange={(e) => handleInputChange(e, game.game_id)}
                           placeholder="Category"
                    />
                    <Select className="gameDetailStyles"
                            name="difficulty"
                            value={editableGames[game.game_id]?.difficulty || game.difficulty}
                            onChange={(e) => handleInputChange(e, game.game_id)}
                            placeholder="Select difficulty"
                    >
                      <option value="Easy">Easy</option>
                      <option value="Medium">Medium</option>
                      <option value="Difficult">Difficult</option>
                    </Select>
                    <Input className="gameDetailStyles"
                           name="no_of_questions"
                           value={editableGames[game.game_id]?.no_of_questions || game.no_of_questions}
                           onChange={(e) => handleInputChange(e, game.game_id)}
                           placeholder="No. of Questions"
                           type="number"
                    />
                    <Input className="gameDetailStyles"
                           name="start_time"
                           value={editableGames[game.game_id]?.start_time || game.start_time}
                           onChange={(e) => handleInputChange(e, game.game_id)}
                           placeholder="Start Time"
                           type="datetime-local"
                    />
                  </>
                )}
              </Box>
            </Collapse>
            <Box>
              {!editableGames[game.game_id] ? (
                <Button
                  leftIcon={<AiOutlineEdit />}
                  colorScheme="teal"
                  size="sm"
                  variant="outline"
                  className="buttonStyles1"
                  onClick={() => toggleEditGame(game.game_id)}
                >
                  Edit
                </Button>
              ) : (
                <Button
                  leftIcon={<AiOutlineEdit />}
                  colorScheme="teal"
                  size="md"
                  variant="outline"
                  onClick={() => handleEditGame(game.game_id)}
                  className="buttonStyles1"
                >
                  Save
                </Button>
              )}
              <Button
                leftIcon={<AiOutlineDelete />}
                colorScheme="red"
                size="md"
                variant="outline"
                onClick={() => handleDeleteGame(game.game_id)}
                className="buttonStyles1"
              >
                Delete
              </Button>
            </Box>
          </Box>
        ))
          )}
        <Flex justify="center" mt={4}>
          {games.length > gamesPerPage && (
            <>
              {Array.from({ length: Math.ceil(games.length / gamesPerPage) }).map((_, index) => (
                <Button
                  key={index}
                  mx={2}
                  variant="outline"
                  colorScheme={currentPage === index + 1 ? 'teal' : 'gray'}
                  onClick={() => paginate(index + 1)}
                >
                  {index + 1}
                </Button>
              ))}
            </>
          )}
        </Flex>
      </Box>
    </Box>
  );
}

export default ShowGames;