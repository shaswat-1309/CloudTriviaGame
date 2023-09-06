import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GameDataContext } from './App';


const WebSocketComponent = () => {
  const { gameData } = useContext(GameDataContext);

  const { game, teamName, userId } = gameData;



  const [socket, setSocket] = useState(null);
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [explanation, setExplanation] = useState('');
  const [isQuestionVisible, setIsQuestionVisible] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [questionNumber, setQuestionNumber] = useState(1);
  const [gameStarted, setGameStarted] = useState(false);
  const [hint, setHint] = useState('');
  const [teamScores, setTeamScores] = useState([]);
  const [isChatBotVisible, setIsChatBotVisible] = useState(false);
  const [isScoreboardVisualizeVisible, setIsScoreboardVisualizeVisible] = useState(false);
  const [messageToSend, setMessageToSend] = useState('');



  useEffect(() => {
    console.log("Inside use effect for web socket connection")
    // Create a new WebSocket connection with gameId, teamName, and userId as query parameters
    const ws_url = "wss://nae0salr16.execute-api.us-east-1.amazonaws.com/production"
    const ws_url_with_query_params = ws_url + `?gameId=${game.gameId}&teamName=${teamName}&userId=${userId}&category=${game.category}`;
    const ws = new WebSocket(ws_url_with_query_params);

    // Event listener for when the connection is established
    ws.onopen = () => {
        console.log('WebSocket connection established.');
        setSocket(ws); // Save the WebSocket instance to state
    };

    // Event listener for incoming messages from the server
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log('Received message:', message);

      // Check if the received message is a question
      if (message.question) {
        setQuestion(message.question);
        setOptions(message.options);
        setQuestionNumber(message.question_number);
        setIsQuestionVisible(true); // Show the question

        // clear answer and explanation
        setCorrectAnswer('');
        setExplanation('');
        setHint('');
        setElapsedTime(0); // Reset elapsed time for each question
        setGameStarted(true);
      } else if (message.answer_details) {
        var answer_details = message.answer_details
        setQuestion(answer_details.question);
        setOptions(answer_details.options);
        setCorrectAnswer(answer_details.correct_option);
        setExplanation(answer_details.explanation);
        if(message.team_scores) {
          setTeamScores(message.team_scores)
        }
        setIsQuestionVisible(false); // Hide the question div and show the answer/explanation div
      } else if(message.hint) {
        setHint(message.hint);
      } else if(message.scoreboard) {
        setQuestion('');
        setOptions('');
        setCorrectAnswer('');
        setExplanation('');
        setTeamScores(message.scoreboard);
        setIsScoreboardVisualizeVisible(true);
      }
    };

    // Event listener for WebSocket errors
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    // Event listener for when the connection is closed
    ws.onclose = () => {
        console.log('WebSocket connection closed.');
        setSocket(null); // Reset the WebSocket instance when connection is closed
        // Redirect to the home page or any other page as needed
        // navigate('/');
    };

    // Clean up the WebSocket connection when the component unmounts
    return () => {
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
    };
  }, []);

  useEffect(() => {

    // Timer to update elapsed time for each question
    const timerInterval = setInterval(() => {
      if (isQuestionVisible) {
        setElapsedTime((prevElapsedTime) => prevElapsedTime + 1);
      }
    }, 1000);

    return () => {
        clearInterval(timerInterval);
    };
  }, [isQuestionVisible]);


  const handleAnswerSubmit = () => {
    if (selectedOption !== null) {
      // Implement the logic to send the chosen option to the backend via WebSocket
      const answerData = {
        questionNumber,
        gameId: game.gameId,
        teamName,
        userId,
        chosenOption: selectedOption,
      };
      const submitAnswer = {
          "action": "submitAnswer",
          "answerDetails": answerData
      }
      console.log("Sending submitAnswer: ",submitAnswer);
      socket.send(JSON.stringify(submitAnswer));
    }
  };


  const handleHintClick = () => {
    // Implement the logic to send hint request to the backend via WebSocket
      const questionDetails = {
        questionNumber,
        gameId: game.gameId,
        teamName,
        userId,
      };
      const hintRequest = {
          "action": "getHint",
          "questionDetails": questionDetails
      }
    socket.send(JSON.stringify(hintRequest));
  };

  const handleMessageSubmit = (e) => {
    e.preventDefault();

    if (messageToSend.trim() !== '') {
      const messageData = {
        gameId: game.gameId,
        teamName,
        userId,
        message: messageToSend.trim(),
      };

      const messageRequest = {
        "action": "sendMessage",
        "messageData": messageData
    }
      socket.send(JSON.stringify(messageRequest));

      // Clear the message input field after sending the message
      setMessageToSend('');
    }
  };

  const handleRedirectToLookerStudioURL = () => {
    // Replace the URL with the external link you want to redirect to
    const lookerURL = 'https://lookerstudio.google.com/embed/reporting/065a6ba8-a7b7-4a13-bfbc-20e8acdec42b/page/GaqYD"';
    window.open(lookerURL, '_blank');
  };

  const handleChatBotClick = () => {
    if(isChatBotVisible)
      setIsChatBotVisible(false);
    else
      setIsChatBotVisible(true);
  };

  const handleExitGame = () => {
    // Close the WebSocket connection
    if (socket) {
        const closeMessage = JSON.stringify({
          action: 'close',
          gameId: game.gameId,
        });
        socket.close(1000, closeMessage);
    }

    // Redirect to the home page or any other page as needed
    navigate('/');
  };

  const navigate = useNavigate();


  const formatTime = (timeInSeconds) => {
    const minutes = Math.floor(timeInSeconds / 60).toString().padStart(2, '0');
    const seconds = (timeInSeconds % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {/* Display game name, category, difficulty, and live scores of teams */}
      <h1>{game.gameName}</h1>
      <p>Category: {game.category}</p>
      <p>Difficulty: {game.difficulty}</p>

      {/* Display live scores of teams */}
      <h2>Live Scores</h2>
      <ul>
        {/* Assume you have an array of team scores with each object having 'teamName' and 'score' */}
        {teamScores.map((teamScore) => (
          <li key={teamScore.team}>
            {teamScore.team}: {teamScore.score}
          </li>
        ))}
      </ul>

      {/* Display welcome message until game is started */}
      {!gameStarted && (
        <div>
          <h2>Welcome to the game - {gameData.game_name}</h2>
          <p>Please wait for the game to start.</p>
        </div>
      )}

      {/* Display question and options */}
      {gameStarted && isQuestionVisible && (
        <div>
          <h2>{questionNumber}: {question}</h2>
          <ol>
            {options.map((option, index) => (
              <li key={index}>
                <input
                  type="radio"
                  name="option"
                  value={index}
                  checked={selectedOption === index}
                  onChange={() => setSelectedOption(index)}
                />
                {option}
              </li>
            ))}
          </ol>
          <p>Time Elapsed: {formatTime(elapsedTime)}</p>
          {hint && (
            <div>
              <h2>Hint requested - {hint}</h2>
            </div>
          )}
          <button onClick={handleAnswerSubmit}>Submit</button>
          <button onClick={handleHintClick}>Hint</button>

        </div>
      )}

      {/* Display correct answer and explanation */}
      {gameStarted && !isQuestionVisible && (
        <div>
          <h2>{question}</h2>
          <ol>
            {options.map((option, index) => (
              <li key={index}>
                {option}
              </li>
            ))}
          </ol>
          <p>Correct Answer: {correctAnswer}</p>
          <p>Explanation: {explanation}</p>
        </div>
      )}

      <form onSubmit={handleMessageSubmit}>
        <input
          type="text"
          value={messageToSend}
          onChange={(e) => setMessageToSend(e.target.value)}
          placeholder="Type your message here..."
        />
        <button type="submit">Send</button>
      </form>

      {/* Display received messages */}
      <div>
        <h3>Received Messages:</h3>
        {/* Your logic to display received messages here */}
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>

          {isChatBotVisible && (

            <iframe
              src="https://d111x2r5ry5wvb.cloudfront.net/index.html"
              width="400"
              height="500"
              title="Chat Bot"
            />
          )}
      </div>

      {isScoreboardVisualizeVisible && (
        <button onClick={handleRedirectToLookerStudioURL}>Visualize scoreboard</button>
      )}

      <button onClick={handleChatBotClick}>Open Chat Bot</button>
      <button onClick={handleExitGame}>Exit Game</button>

    </div>
  );
};

export default WebSocketComponent;
