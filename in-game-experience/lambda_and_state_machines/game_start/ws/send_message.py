import json
import boto3
import os

api_gateway_management_api = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ['ENDPOINT_URL'])


# get hint request from game participants, hint is broadcast to all the team members
def lambda_handler(event, context):
    print(event)
    event_body = json.loads(event['body'])
    chat_details = event_body['messageData']

    # extract game, team and q no for retrieving the hint
    game_id = chat_details['gameId']
    team = chat_details['teamName']

    print("chat_details:", chat_details)

    # extract the user details and message and broadcast to the whole team
    chat_message = {
        "user_id" : chat_details['userId'],
        "message": chat_details['message']
    }

    chat_message_response = json.dumps(chat_message)
    # broadcast to all team members
    broadcast_to_team(game_id, team, chat_message_response)

    return {
        'statusCode': 200,
        'body': chat_message_response
    }


# broadcast the hint to the whole team
def broadcast_to_team(game_id, team, chat_message):
    # get all team participants in the game
    team_participants_connections = get_connections_for_game_and_team(game_id, team)
    print("team_participants_connections", team_participants_connections)

    # loop and send message to all team member's connection
    for connection in team_participants_connections:
        connection_id = connection['connection_id']
        print(connection_id)
        try:
            api_gateway_management_api.post_to_connection(ConnectionId=connection_id, Data=chat_message)
            print("message sent")
        except Exception as e:
            print('Error sending message to connection:', e)


# get connections related to a team
def get_connections_for_game_and_team(game_id, team):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameParticipants')

    # use index to filter the specific team details
    response = table.query(
        IndexName='GameIdTeamIndex',  # GameIdTeamIndex is Global Secondary Index (GSI) containing game_id and team attributes
        KeyConditionExpression='game_id = :game_id_val and team = :team_val',
        ExpressionAttributeValues={
            ':game_id_val': game_id,
            ':team_val': team
        }
    )

    print("GameIdTeamIndex", response)
    connections = response['Items']

    return connections

