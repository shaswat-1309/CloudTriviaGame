import React, { useEffect, useState } from 'react';
import { Box, Button, FormControl, FormLabel, Input, Select, Text } from '@chakra-ui/react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../App.css';

function CreateGame() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('https://us-central1-serverlessproject-392714.cloudfunctions.net/fetchcategories');
        const categoriesResponse = response.data;

        if (categoriesResponse.length > 0) {
          const categories = categoriesResponse[0].categories;
          setCategories(categories || []);
        }

        setLoading(false);
      } catch (error) {
        console.error(error);
      }
    };

    fetchCategories();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const form = event.target;
    const rawStartTime = form.start_time.value; // Get the raw datetime string from the form input
    const utcStartTime = new Date(`${rawStartTime}Z`).toISOString();

    const formData = {
      game_name: form.game_name.value,
      category: form.category.value,
      difficulty: form.difficulty.value,
      start_time: utcStartTime,
      no_of_questions: form.no_of_questions.value,
    };

    try {
      const response = await axios.post(
        '${process.env.REACT_APP_API_GATEWAY_URL}/CreateGame',
        formData
      );
      console.log(response.data); // Handle the response as needed
      alert('Game created successfully!');
      navigate('/');
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <Box className="containerStyles">
      <Box className="navbarStyles">
        <Link to="/" className="backButtonStyles">
          Back
        </Link>
        <Text as="h1" className="logoStyles">
          Create Game
        </Text>
      </Box>
      <form onSubmit={handleSubmit}>
        <FormControl id="game_name" isRequired className="formControlStyles">
          <FormLabel>Game Name</FormLabel>
          <Input type="text" name="game_name" />
        </FormControl>

            <FormControl id="category" isRequired className="formControlStyles">
              <FormLabel>Category</FormLabel>
              <Select placeholder="Select category" name="category" disabled={loading}
                      style={{ width: '200px', height: '40px', fontSize: '15px' }}>
                {categories && categories.length > 0 ? (
                  categories.map((category) => (
                    <option key={category} value={category}>
                      {category}
                    </option>
                  ))
                ) : (
                  <option value="">No categories found</option>
                )}
              </Select>
            </FormControl>

        <FormControl id="difficulty" isRequired className="formControlStyles">
          <FormLabel>Difficulty</FormLabel>
          <Select placeholder="Select difficulty" name="difficulty"
                  style={{ width: '200px', height: '40px', fontSize: '15px' }}>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Difficult">Difficult</option>
          </Select>
        </FormControl>

        <FormControl id="start_time" isRequired className="formControlStyles">
          <FormLabel>Start Time</FormLabel>
          <Input type="datetime-local" name="start_time" />
        </FormControl>

        <FormControl id="no_of_questions" isRequired className="formControlStyles">
          <FormLabel>Number of Questions</FormLabel>
          <Input type="number" min={1} name="no_of_questions" />
        </FormControl>

        <Button colorScheme="teal" className="submitButtonStyles" type="submit">
          Submit
        </Button>
      </form>
    </Box>
  );
}

export default CreateGame;
