import os
import requests


def lambda_handler(event, context):
    fetch_question_url = os.environ['FETCH_QUESTION_URL']

    try:

        # get the game questions by calling the cloud function (questions table is in firestore)
        game_questions_response = requests.post(fetch_question_url, json=event)

        if game_questions_response.status_code == 200:
            game_questions = game_questions_response.json()
            print(game_questions)
            event['game_questions'] = game_questions['questions']
        else:
            print(f"API call failed with status code: {game_questions_response.status_code}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

    return event
