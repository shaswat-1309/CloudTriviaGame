import boto3
import os

dynamodb = boto3.resource('dynamodb')
game_table = os.environ['DYNAMODB_TABLE_NAME']
table = dynamodb.Table(game_table)

def lambda_handler(event, context):
    # Retrieve the game ID from the event payload
    request_json = event
    game_id = request_json['game_id']

    # Delete the game from the DynamoDB table
    table.delete_item(Key={'game_id': game_id})

    return {
        'statusCode': 200,
        'body': {'message': 'Game deleted successfully'}
    }
