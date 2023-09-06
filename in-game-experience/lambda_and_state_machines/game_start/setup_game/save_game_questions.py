import json
import boto3
import os


def lambda_handler(event, context):
    print(event)

    # get the game and question details from the event
    game_id = event['game_id']
    game_questions = event['game_questions']

    dynamodb_client = boto3.client('dynamodb', region_name=os.environ['REGION'])

    try:
        # iterate and save the questions in the GameQuestions table
        for question_number, question_details in enumerate(game_questions, start=1):
            print(question_number)
            print(question_details)

            dynamodb_client.put_item(
                TableName='GameQuestions',
                Item={
                    'game_id': {'S': game_id},
                    'question_number': {'N': str(question_number)},
                    'question': {'S': question_details['question']},
                    'options': {'L': [{'S': option} for option in question_details['options']]},
                    'correct_option': {'N': str(question_details['correct_option'])},
                    'hint': {'S': question_details['hint']},
                    'explanation': {'S': question_details['explanation']}
                }
            )

    except Exception as e:
        print(f"Exception {e} occurred!")

    return event

