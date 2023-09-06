import boto3
import json
import os


# apigatewaymanagementapi client by passing websocket url to broadcast the message to open connections
apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ['ENDPOINT_URL'])


def lambda_handler(event, context):
    print("orig event", event)

    game_id = event['game_id']

    # fetch all connections from the GameParticipants table
    game_participant_connections = get_game_participants(game_id)
    print('game_participant_connections', game_participant_connections)

    # team scores are already present in the event
    # (while showing answers live scores are also fetched)
    scoreboard = {
        "scoreboard": event['team_scores']
    }
    scoreboard_str = json.dumps(scoreboard)

    # Loop through each game participant connection and send the message
    for connection_id in game_participant_connections:
        print("participant connection_id", connection_id)
        send_message_to_connection(connection_id, scoreboard_str)

    return event


# sending message to the game participant connection
def send_message_to_connection(connection_id, message):
    try:
        apigatewaymanagementapi.post_to_connection(ConnectionId=connection_id, Data=message)
        print("message sent")
    except Exception as e:
        print('Error sending message to connection:', e)


# get the game participant for the current game
def get_game_participants(game_id):
    # Query the GameParticipants table to get participants by filtering on gameId
    dynamodb_client = boto3.resource('dynamodb', region_name=os.environ['REGION'])

    game_participants_table = dynamodb_client.Table('GameParticipants')  # Replace with your table name

    # Query the GameParticipants table to get all participants' connection IDs for the game_id
    response = game_participants_table.query(
        KeyConditionExpression='game_id = :game_id',
        ExpressionAttributeValues={':game_id': game_id}
    )

    # Extract the connection IDs from the response
    connection_ids = [item['connection_id'] for item in response['Items']]

    print(connection_ids)
    return connection_ids
