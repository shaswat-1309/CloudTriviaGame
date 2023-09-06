import React, { useEffect, useState } from 'react';
import { Box, Collapse, Text, Button, Flex, Input, Select } from '@chakra-ui/react';
import { AiOutlineDown, AiOutlineUp, AiOutlineEdit, AiOutlineDelete } from 'react-icons/ai';
import axios from 'axios';
import '../App.css';
import { Link } from 'react-router-dom';

function ShowQuestions() {
  const [questions, setQuestions] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [questionsPerPage] = useState(2);
  const [loading, setLoading] = useState(true)


  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('https://us-central1-serverlessproject-392714.cloudfunctions.net/showquestions');
        // Check if there are no questions to show
        setQuestions(response.data.questions || []);
        // Check if there are no questions to show
      } catch (error) {
        console.error(error);
      }
      finally {
        setLoading(false); // Set loading state to false after API call is completed
      }
    };

    fetchQuestions();
  }, []);
  
  const [showDetails, setShowDetails] = useState({});
  const [editableQuestions, setEditableQuestions] = useState({});

  const toggleDetails = (questionId) => {
    setShowDetails((prevState) => ({
      ...prevState,
      [questionId]: !prevState[questionId]
    }));
  };

  const toggleEditQuestion = (questionId) => {
    setEditableQuestions((prevState) => ({
      ...prevState,
      [questionId]: !prevState[questionId]
    }));
  };

  const handleEditQuestion = async (questionId) => {
    try {
      const updatedQuestion = editableQuestions[questionId];
      // Make API call to edit question
      const response = await axios.post('https://us-central1-serverlessproject-392714.cloudfunctions.net/editquestion', {
        id: questionId,
        question: updatedQuestion.question,
        options: updatedQuestion.options.split(','), // Convert options to list
        correct_option: updatedQuestion.correct_option,
        difficulty: updatedQuestion.difficulty,
        hint: updatedQuestion.hint,
        explanation: updatedQuestion.explanation,
        category: updatedQuestion.category
      } );
      console.log(response.data); // Handle the response as needed
      // Refresh questions list
      const questionsResponse = await axios.get('https://us-central1-serverlessproject-392714.cloudfunctions.net/showquestions'
        );
      setQuestions(questionsResponse.data.questions || []);
      toggleEditQuestion(questionId); // Disable editing mode after updating the question
    } catch (error) {
      console.error(error);
    }
  };
  const handleDeleteQuestion = async (id) => {
    try {
      // Make API call to delete question
      const response = await axios.post('https://us-central1-serverlessproject-392714.cloudfunctions.net/deletequestion',
        { document_id: id }
      );
      console.log(response.data); // Handle the response as needed
      // Refresh questions list
      const questionsResponse = await axios.get('https://us-central1-serverlessproject-392714.cloudfunctions.net/showquestions'
        );
      setQuestions(questionsResponse.data.questions || []);
    } catch (error) {
      console.error(error);
    }
  };

  const handleInputChange = (e, questionId) => {
    const { name, value } = e.target;
    setEditableQuestions((prevState) => ({
      ...prevState,
      [questionId]: {
        ...prevState[questionId],
        [name]: value
      }
    }));
  };

  const indexOfLastQuestion = currentPage * questionsPerPage;
  const indexOfFirstQuestion = indexOfLastQuestion - questionsPerPage;
  const currentQuestions = questions.slice(indexOfFirstQuestion, indexOfLastQuestion);

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
          Questions List
        </Text>
      </Box>
      <Box className="questionsListStyles">
        {/* Conditional rendering for no questions */}
        {loading ? (
          <>
            <Text as="h3" className="logoStyles1">
              Loading...
            </Text>
            {/* Add your loading symbol here */}
          </>
        ) : questions.length === 0 ? (
          <>
            <Text as="h3" className="logoStyles1">
              No questions created
            </Text>
            <Button
              as={Link}
              to="/addquestion"
              colorScheme="teal"
              size="sm"
              variant="outline"
              className="ButtonStyles2"
            >
              Create Question
            </Button>
          </>
        ) : (
          currentQuestions.map((question, index) => (
            <Box key={question.question_id} className="questionItemStyles">
              <Box display="flex" alignItems="center" className="questionHeaderStyles">
                <Text as="h3" className="questionTextStyles">
                  {index + 1 + (currentPage - 1) * questionsPerPage}.{' '}
                  {!editableQuestions[question.question_id] ? (
                    question.question
                  ) : (
                    <Input className="questionDetailStyles"
                           name="question"
                           value={editableQuestions[question.question_id]?.question || question.question}
                           onChange={(e) => handleInputChange(e, question.question_id)}
                           placeholder="Question"
                    />
                  )}
                </Text>
                {showDetails[question.question_id] ? (
                  <AiOutlineUp onClick={() => toggleDetails(question.question_id)} className="chevronIconStyles" />
                ) : (
                  <AiOutlineDown onClick={() => toggleDetails(question.question_id)} className="chevronIconStyles" />
                )}
              </Box>
              <Collapse in={showDetails[question.question_id]} animateOpacity>
                <Box mt={2} className="questionDetailsStyles">
                  {!editableQuestions[question.question_id] ? (
                    <>
                      <Text className="questionDetailStyles">Category: {question.category}</Text>
                      <Text className="questionDetailStyles">Options: {question.options}</Text>
                      <Text className="questionDetailStyles">Correct Option: {question.correct_option}</Text>
                      <Text className="questionDetailStyles">Difficulty: {question.difficulty}</Text>
                      <Text className="questionDetailStyles">Hint: {question.hint}</Text>
                      <Text className="questionDetailStyles">Explanation: {question.explanation}</Text>
                    </>
                  ) : (
                    <>
                      <Input
                            className="questionDetailStyles"
                            name="category"
                            value={editableQuestions[question.question_id]?.category || question.category}
                            onChange={(e) => handleInputChange(e, question.question_id)}
                            placeholder="Category"
                      />
                      <Input className="questionDetailStyles"
                             name="options"
                             value={editableQuestions[question.question_id]?.options || question.options}
                             onChange={(e) => handleInputChange(e, question.question_id)}
                             placeholder="Options"
                      />
                      <Input className="questionDetailStyles"
                             name="correct_option"
                             value={editableQuestions[question.question_id]?.correct_option || question.correct_option}
                             onChange={(e) => handleInputChange(e, question.question_id)}
                             placeholder="Correct Option"
                      />
                      <Select className="questionDetailStyles"
                              name="difficulty"
                              value={editableQuestions[question.question_id]?.difficulty || question.difficulty}
                              onChange={(e) => handleInputChange(e, question.question_id)}
                              placeholder="Select difficulty"
                      >
                        <option value="Easy">Easy</option>
                        <option value="Medium">Medium</option>
                        <option value="Difficult">Difficult</option>
                      </Select>
                      <Input className="questionDetailStyles"
                             name="hint"
                             value={editableQuestions[question.question_id]?.hint || question.hint}
                             onChange={(e) => handleInputChange(e, question.question_id)}
                             placeholder="Hint"
                      />
                      <Input className="questionDetailStyles"
                             name="explanation"
                             value={editableQuestions[question.question_id]?.explanation || question.explanation}
                             onChange={(e) => handleInputChange(e, question.question_id)}
                             placeholder="Explanation"
                      />
                    </>
                  )}
                </Box>
              </Collapse>
              <Box className="questionButtonsStyles">
                {!editableQuestions[question.question_id] ? (
                  <Button
                    leftIcon={<AiOutlineEdit />}
                    colorScheme="teal"
                    size="lg"
                    variant="outline"
                    onClick={() => toggleEditQuestion(question.question_id)}
                    className="buttonStyles1"
                  >
                    Edit
                  </Button>
                ) : (
                  <Button
                    leftIcon={<AiOutlineEdit />}
                    colorScheme="teal"
                    size="lg"
                    variant="outline"
                    onClick={() => handleEditQuestion(question.question_id)}
                    className="buttonStyles1"
                  >
                    Save
                  </Button>
                )}
                <Button
                  leftIcon={<AiOutlineDelete />}
                  colorScheme="red"
                  size="lg"
                  variant="outline"
                  onClick={() => handleDeleteQuestion(question.question_id)}
                  className="buttonStyles1"
                >
                  Delete
                </Button>
              </Box>
            </Box>
          ))
        )}
        <Flex justify="center" mt={4}>
          {Array.from({ length: Math.ceil(questions.length / questionsPerPage) }).map((_, index) => (
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
        </Flex>
      </Box>
    </Box>
  );
};


export default ShowQuestions;
