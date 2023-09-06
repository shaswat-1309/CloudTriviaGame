from google.cloud import firestore
from google.cloud import language_v1
from flask import jsonify, make_response

# Initialize Firestore and Language API clients
db = firestore.Client.from_service_account_json("serviceKey.json")
language_client = language_v1.LanguageServiceClient.from_service_account_json("serviceKey.json")

def showquestions(request):
    try:

        if request.method == 'OPTIONS':
            # Handle preflight request for CORS
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'GET')
            return response

        if request.method == 'GET':
            # Fetch all the questions from the Firestore collection
            questions_ref = db.collection('questions').get()

            # Create an empty list to store the questions
            questions = []

            # Iterate through the documents and extract the question and other fields
            for doc in questions_ref:
                question_data = {
                    'question_id': doc.id,
                    'question': doc.get('question'),
                    'options': doc.get('options'),
                    'correct_option': doc.get('correct_option'),
                    'difficulty': doc.get('difficulty'),
                    'hint': doc.get('hint'),
                    'explanation': doc.get('explanation'),
                    'category': doc.get('category')
                }
                questions.append(question_data)

            response = jsonify({'questions': questions})

            # Add CORS headers to the response
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'GET')

            return response

        else:
            return ('Method not allowed', 405)

    except Exception as e:
        return (f'Error occurred: {e}', 500)
