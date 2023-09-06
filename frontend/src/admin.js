import React, { useState } from 'react';
import { Box, Button, Flex, Text } from '@chakra-ui/react';
import { useNavigate, Link } from 'react-router-dom';
import './App.css';
import axios from 'axios';

function Admin() {
  const navigate = useNavigate();
  const [showVisualize, setShowVisualize] = useState(false);

  const handleCreateGame = () => {
    navigate('/create_game');
  };

  const handleAddQuestion = () => {
    navigate('/addquestion');
  };

  const handleShowGames = () => {
    navigate('/showgames');
  };

  const handleVisualize = () => {
    setShowVisualize(true);
  };
  const handleRefresh = async () => {
    try {
      // Make API call to the Cloud Function
      const response = await axios.post('https://us-central1-serverlessproject-392714.cloudfunctions.net/fetchCSV');
      console.log(response); // Handle the response as needed

      // Check if the response contains the specific string
      if (response.data === "CSV file successfully uploaded to Google Cloud Storage!") {
        // If the response matches, reload the Looker report
        setShowVisualize(false); // Hide the visualization
        setTimeout(() => {
          setShowVisualize(true); // Show the visualization after a short delay
        }, 100); // Adjust the delay time as needed
      }
    } catch (error) {
      console.error(error);
    }
  };

    const handleShowQuestions = () => {
    navigate('/showquestions');
  };

  const handleLogout = async () => {
    // ... existing handleLogout logic
  };

  const handleBack = () => {
    setShowVisualize(false);
  };

  return (
    <Box className="containerStyles">
      <Box className="navbarStyles">
        <Link to="/" className="backButtonStyles" onClick={handleLogout}>
          Logout
        </Link>
        <Text className="logoStyles">Triviamania</Text>
      </Box>

      {!showVisualize && (
        <>
          <Flex direction="row" justify="center" className="buttonContainerStyles">
            <Button
              colorScheme="teal"
              size="lg"
              mb={4}
              className="buttonStyles"
              onClick={handleCreateGame}
            >
              Create Game
            </Button>
            <Button
              colorScheme="teal"
              size="lg"
              className="buttonStyles"
              onClick={handleAddQuestion}
            >
              Add Questions
            </Button>
          </Flex>
          <Flex direction="row" justify="center" className="buttonContainerStyles">
            <Button
              colorScheme="teal"
              size="lg"
              mb={4}
              className="buttonStyles"
              onClick={handleShowGames}
            >
              Show Games
            </Button>
            <Button
              colorScheme="teal"
              size="lg"
              className="buttonStyles"
              onClick={handleShowQuestions}
            >
              Show Questions
            </Button>
          </Flex>
          <Flex direction="row" justify="center" className="buttonContainerStyles">
            <Button
              colorScheme="teal"
              size="lg"
              className="buttonStyles"
              onClick={handleVisualize}
            >
              Visualize
            </Button>
          </Flex>
        </>
      )}

      {showVisualize && (
        <Flex direction="column" alignItems="center">
          <iframe
            title="Looker Studio Report"
            src="https://lookerstudio.google.com/embed/reporting/30e485ab-2326-41d4-a343-3cdcf04bb1c3/page/wE3YD"
            width="300"
            height="300"
            allowFullScreen
          />
          <Flex direction="row" justify="center">
            <Button
              colorScheme="teal"
              size="lg"
              className="buttonStyles"
              onClick={handleBack}
            >
              Back
            </Button>
            <Button
              colorScheme="teal"
              size="lg"
              className="buttonStyles"
              onClick={handleRefresh}
            >
              Refresh
            </Button>
          </Flex>
        </Flex>
      )}
    </Box>
  );
}

export default Admin;
