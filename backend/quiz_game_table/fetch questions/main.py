from google.cloud import firestore
import json
import random
import boto3

# Create an instance of the Firestore client
db = firestore.Client.from_service_account_json("serviceKey.json")

def fetchgamequestions(request):
    # Retrieve the game data from the request JSON payload
    request_json = request.get_json()
    category = request_json['category']
    difficulty = request_json['difficulty']
    no_of_questions = request_json['no_of_questions']

    # Fetch questions based on matching category and difficulty from Firestore using queries
    questions_ref = db.collection('questions').where('category', '==', category).where('difficulty', '==', difficulty).get()
    questions = [question.to_dict() for question in questions_ref]
    print(questions)

    # Shuffle the questions and select the required number of questions
    random.shuffle(questions)
    selected_questions = questions[:min(len(questions), no_of_questions)]
    print(selected_questions)
    return {'questions': selected_questions}
