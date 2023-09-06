import boto3
import os

game_table = os.environ['DYNAMODB_TABLE_NAME']

def lambda_handler(event, context):
    # Assuming the DynamoDB table name is 'your_table_name'
    dynamodb = boto3.resource(game_table)
    table = dynamodb.Table('quiz_game_table')

    # Scan the DynamoDB table to fetch all games
    response = table.scan()

    # Extract game names and game IDs from the response
    games = []
    for item in response['Items']:
        game_id = item['game_id']
        game_name = item['game_name']  # Modify the game name format as per your requirement
        category = item['category']
        start_time = item['start_time']
        difficulty = item['difficulty']
        no_of_questions = item['no_of_questions']
        games.append({
            'game_id': game_id,
            'game_name': game_name,
            'category': category,
            'start_time': start_time,
            'difficulty': difficulty,
            'no_of_questions': no_of_questions
        })

    return {'games': games}