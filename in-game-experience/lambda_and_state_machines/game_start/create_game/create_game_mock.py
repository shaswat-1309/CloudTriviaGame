import json
import boto3
from datetime import datetime, timedelta


# TODO to be integrated with Shaswat's admin module - create game lambda
def lambda_handler(event, context):
    print(event)

    game_start_time = event['start_time']

    # format the game_start_time (ignore the above 2 lines in admin create game ())
    # formatted_time = game_start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    lambda_client = boto3.client('lambda')

    try:
        payload = {
            "game_id": event['game_id'],
            "game_name": event['game_name'],
            "no_of_questions": event['no_of_questions'],
            "category": event['category'],
            "difficulty": event['difficulty'],
            "question_number": 1,
            "start_time": game_start_time
        }

        create_game_event_rule = 'create_game_event_rule'
        response = lambda_client.invoke(
            FunctionName=create_game_event_rule,
            InvocationType='Event',
            Payload=json.dumps(payload),
        )

        return {
            'statusCode': 200,
            'body': 'Source Lambda executed successfully!',
        }

    except Exception as e:
        print('Error invoking target_lambda:', e)
        return {
            'statusCode': 500,
            'body': 'Error invoking target_lambda.',
        }

