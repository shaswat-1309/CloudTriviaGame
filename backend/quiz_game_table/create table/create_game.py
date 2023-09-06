import json
import uuid
import boto3
import os

# Create an instance of the DynamoDB resource and provide the AWS configuration
dynamodb = boto3.resource('dynamodb')
game_table = os.environ['DYNAMODB_TABLE_NAME']

table = dynamodb.Table(game_table)

def lambda_handler(event, context):
    # Retrieve the category and starting time from the request JSON payload
    game_name = event['game_name']
    category = event['category']
    start_time = event['start_time']
    difficulty = event['difficulty']
    no_of_questions = event['no_of_questions']
    # Generate a unique game ID for the new game
    game_id = str(uuid.uuid4())

    # Store the game data in DynamoDB
    table.put_item(Item={'game_id': game_id, 'game_name':game_name, 'category': category, 'start_time': start_time,
                         'difficulty': difficulty, 'no_of_questions': no_of_questions, 'status':'Upcoming'})

    # Return the game ID to the client
    return {
        'statusCode': 200,
        'body': json.dumps({'game_id': game_id})
    }
