import json
import uuid
import boto3

# Create an instance of the DynamoDB resource and provide the AWS configuration
dynamodb = boto3.resource('dynamodb')

table_name = 'quiz_game_table'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    # Retrieve the category and starting time from the request JSON payload
    request_json = event
    game_name = request_json['game_name']
    category = request_json['category']
    start_time = request_json['start_time']
    difficulty = request_json['difficulty']
    no_of_questions = request_json['no_of_questions']
    # Generate a unique game ID for the new game
    game_id = str(uuid.uuid4())

    # Store the game data in DynamoDB
    table.put_item(Item={'game_id': game_id, 'game_name': game_name, 'category': category, 'start_time': start_time,
                         'difficulty': difficulty, 'no_of_questions': no_of_questions, 'status': "Upcoming"})

    lambda_client = boto3.client('lambda')

    payload = {
        "game_id": game_id,
        "game_name": game_name,
        "no_of_questions": no_of_questions,
        "category": category,
        "difficulty": difficulty,
        "question_number": 1,
        "start_time": start_time
    }

    create_game_event_rule = 'create_game_event_rule'
    response = lambda_client.invoke(
        FunctionName=create_game_event_rule,
        InvocationType='Event',
        Payload=json.dumps(payload),
    )

    print(response)

    # Return the game ID to the client
    return {
        'statusCode': 200,
        'body': json.dumps({'game_id': game_id})
    }
