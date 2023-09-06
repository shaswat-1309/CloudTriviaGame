import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
game_participants_table = dynamodb.Table('GameParticipants')

# apigatewaymanagementapi client by passing websocket url to broadcast the message to open connections
apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ['ENDPOINT_URL'])


def lambda_handler(event, context):
    game_id = event['game_id']
    next_question_number = event['question_number']

    try:
        # fetch all connections from the GameParticipants table
        get_game_participant_connection_ids = get_game_participants(game_id)

        print('get_game_participant_connection_ids', get_game_participant_connection_ids)

        # delete connection entries from the table
        delete_game_participant_connections(game_id, get_game_participant_connection_ids)

        # loop through each connection and delete/disconnect the connection
        for connection_id in get_game_participant_connection_ids:
            try:
                print(f"Deleting connection {connection_id}")
                apigatewaymanagementapi.delete_connection(ConnectionId=connection_id)
            except Exception as e:
                print(f'Error deleting the connection {connection_id}:', e)
    except Exception as e:
        print('Error in disconnecting participants:', e)

    return event


# get the game participant for the current game
def get_game_participants(game_id):
    # Query the gameparticipants table to get all participants' connection IDs for the game_id
    response = game_participants_table.query(
        KeyConditionExpression='game_id = :game_id',
        ExpressionAttributeValues={':game_id': game_id}
    )

    # Extract the connection IDs from the response
    connection_ids = [item['connection_id'] for item in response['Items']]

    print(connection_ids)
    return connection_ids


# delete all the game connections from DB once the game is over
def delete_game_participant_connections(game_id, connection_ids):
    # Delete all the entries for the game_id from the gameparticipants table
    with game_participants_table.batch_writer() as batch:
        for connection_id in connection_ids:
            batch.delete_item(Key={'game_id': game_id, 'connection_id': connection_id})
