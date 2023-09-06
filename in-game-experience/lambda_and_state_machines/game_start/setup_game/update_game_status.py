import json
import boto3


# TODO remove the sample event
# {"game_id": "game2", "game_name": "game2", "no_of_questions": 4, "category": "Miscellaneous", "difficulty": "Easy", "question_number": 1, "start_time": "2023-07-21T22:10:00Z"}

def lambda_handler(event, context):
    print(event)
    try:

        actual_event = event['input']
        game_id = actual_event['game_id']

        # get the game status to be updated from the event (this is manipulated in the workflows/step functions)
        # can be In progress, Waiting or Completed
        if 'game_status' in event:
            game_status = event['game_status']
            update_game_status(game_id, game_status)
            del event['game_status']

        else:
            print("game_status not present!")

    except Exception as e:
        print(f"Exception {e} occurred!")

    return actual_event


# update the quiz_game_table with the new game status
def update_game_status(game_id, game_status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('quiz_game_table')

    # update the status field in the table for the given game_id
    response = table.update_item(
        Key={'game_id': game_id},
        UpdateExpression='SET #s = :status_val',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':status_val': game_status}
    )

    print(response)
