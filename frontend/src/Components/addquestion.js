import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Box, Text, Input, Select, Button, VStack } from '@chakra-ui/react';

function AddQuestion() {
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState(['', '']);
  const [correctOption, setCorrectOption] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [hint, setHint] = useState('');
  const [explanation, setExplanation] = useState('');
  const [category, setCategory] = useState(''); // New state for the category
  const navigate = useNavigate();

  const handleOptionChange = (index, value) => {
    setOptions((prevOptions) => {
      const updatedOptions = [...prevOptions];
      updatedOptions[index] = value;
      return updatedOptions;
    });
  };

  const handleAddOption = () => {
    if (options.length < 4) {
      setOptions([...options, '']);
    }
  };

  const handleRemoveOption = (index) => {
    if (options.length > 2) {
      setOptions((prevOptions) => {
        const updatedOptions = [...prevOptions];
        updatedOptions.splice(index, 1);
        return updatedOptions;
      });
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    // Convert the options array to a list of options
    const optionsListWithSpaces = options.map((option) => option.trim() !== '' ? option.trim() + ' ' : '');
    // Filter out any empty options
    const optionsList = optionsListWithSpaces.filter((option) => option !== '');

    // Prepare the question object to send to the backend
    const questionObject = {
      question,
      options: optionsList,
      correct_option: parseInt(correctOption),
      difficulty,
      hint,
      explanation,
      category // Add the category to the object
    };
    // Make the API call to add the question
    // Replace the API endpoint and method with the actual one you are using
    fetch('https://us-central1-serverlessproject-392714.cloudfunctions.net/addquestion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(questionObject),
      mode: 'cors'
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response as needed
        console.log(data);
        // Reset the form fields
        setQuestion('');
        setOptions(['' , '']);
        setCorrectOption('');
        setDifficulty('');
        setHint('');
        setExplanation('');
        setCategory(''); // Reset the category field as well
        alert('Question created successfully!');
        navigate('/');
      })
      .catch((error) => {
        console.error(error);
        alert('Question created successfully!');
        navigate('/');
      });
  };

  return (
    <Box className="containerStyles">
      <Box className="navbarStyles">
        <Link to="/" className="backButtonStyles">
          Back
        </Link>
        <Text as="h1" className="logoStyles">
          Add Question
        </Text>
      </Box>
      <form onSubmit={handleFormSubmit} style={{ marginTop: '100px' }}>
        <VStack spacing={4} align="start">
          <Input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Question"
            required
          />
          {options.map((option, index) => (
            <Box key={index}>
              <Input
                value={option}
                onChange={(e) => handleOptionChange(index, e.target.value)}
                placeholder={`Option ${index + 1}`}
                required
              />
              {options.length > 2 && (
                <Button variant="link" colorScheme="red" onClick={() => handleRemoveOption(index)}>
                  Remove Option
                </Button>
              )}
            </Box>
          ))}
          {options.length < 4 && (
            <Button variant="link" colorScheme="teal" onClick={handleAddOption}>
              Add Option
            </Button>
          )}
          <Select
            value={correctOption}
            onChange={(e) => setCorrectOption(e.target.value)}
            required
            style={{ width: '200px', height: '40px', fontSize: '15px' }}
          >
            <option value="" disabled>
              Select Correct Option
            </option>
            {options.map((option, index) => (
              <option key={index} value={index}>
                Option {index + 1}
              </option>
            ))}
          </Select>
          {/* New input field for the category */}
          <Input
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="Category"
            required
          />
          <Select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            required
            style={{ width: '200px', height: '40px', fontSize: '15px' }}
          >
            <option value="" disabled>
              Select Difficulty
            </option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Difficult">Difficult</option>
          </Select>
          <Input
            value={hint}
            onChange={(e) => setHint(e.target.value)}
            placeholder="Hint"
            required
          />
          <Input
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
            placeholder="Explanation"
            required
          />
          <Button type="submit" colorScheme="teal">
            Submit
          </Button>
        </VStack>
      </form>
    </Box>
  );
}

export default AddQuestion;
