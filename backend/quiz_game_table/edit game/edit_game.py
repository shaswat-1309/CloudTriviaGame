import boto3
import os


dynamodb = boto3.resource('dynamodb')
game_table = os.environ['DYNAMODB_TABLE_NAME']
table = dynamodb.Table(game_table)

def lambda_handler(event, context):
    # Retrieve the game ID from the event payload
    request_json = event
    print(event)
    game_id = request_json['game_id']

    # Retrieve the updated game details from the request JSON payload
    updated_game = request_json.copy()  # Create a copy of the request data

    # Remove the game_id field from the updated_game dictionary
    updated_game.pop('game_id', None)

    # Retrieve the current game data from the DynamoDB table
    response = table.get_item(Key={'game_id': game_id})
    current_game = response.get('Item', {})

    # Update only the changed fields in the current_game dictionary
    for field, value in updated_game.items():
        if field in current_game and current_game[field] != value:
            current_game[field] = value

    # Update the game data in the DynamoDB table
    table.update_item(
        Key={'game_id': game_id},
        UpdateExpression='SET game_name = :name, category = :category, start_time = :start_time, difficulty = :difficulty, no_of_questions = :no_of_questions',
        ExpressionAttributeValues={
            ':name': current_game.get('game_name'),
            ':category': current_game.get('category'),
            ':start_time': current_game.get('start_time'),
            ':difficulty': current_game.get('difficulty'),
            ':no_of_questions': current_game.get('no_of_questions')
        }
    )

    return {
        'statusCode': 200,
        'body': current_game
    }