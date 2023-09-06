import json
import boto3
import os

api_gateway_management_api = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ['ENDPOINT_URL'])


# get hint request from game participants, hint is broadcast to all the team members
def lambda_handler(event, context):
    print(event)
    event_body = json.loads(event['body'])
    question_details = event_body['questionDetails']

    print("question_details response:", question_details)

    # extract game, team and q no for retrieving the hint
    game_id = question_details['gameId']
    team = question_details['teamName']
    question_number = question_details['questionNumber']

    # hint limit exceeded message
    hint = "Hint limit exceeded for the team"

    # get the hint used by the team for the current fame
    hint_used = get_hint_used_list(game_id, team)
    print("hint_used already", hint_used)

    # check if hint used for the game is less than 2 or the hint has already been requested for the current ques
    if len(hint_used) < 2 or question_number in hint_used:

        # if the conditions match get the hint for the current ques from the DB
        hint = get_hint_of_question(game_id, question_number)

        # update the hint used list for the team for the current game
        if hint != '':
            update_hint_used(game_id, team, question_number)

    hint_response = {
        'hint': hint
    }
    hint_response_message = json.dumps(hint_response)

    # broadcast to all team members
    broadcast_to_team(game_id, team, hint_response_message)

    return {
        'statusCode': 200,
        'body': hint_response_message
    }


# get the hint used list from Scoreboard table to see if hint limit is exceeded or not
def get_hint_used_list(game_id, team):
    dynamodb_client = boto3.client('dynamodb')

    # fetch the hint used list for the team from the scoreboard item
    response = dynamodb_client.get_item(
        TableName='Scoreboard',
        Key={
            'game_id': {'S': game_id},
            'team': {'S': team}
        },
        ProjectionExpression='hint_used'
    )

    # extract and return the hint used list value
    hint_used_list = response['Item'].get('hint_used', {'NS': []})
    return set(map(int, hint_used_list.get('NS', [])))


# fetch the hint for the game question
def get_hint_of_question(game_id, question_no):
    hint = ""
    dynamodb_client = boto3.client('dynamodb')

    # fetch hint for the question
    response = dynamodb_client.get_item(
        TableName='GameQuestions',
        Key={
            'game_id': {'S': game_id},
            'question_number': {'N': str(question_no)}
        },
        ProjectionExpression='hint'
    )

    # extract hint from the get item response
    if response['Item']['hint']:
        hint = response['Item']['hint']['S']

    return hint


# update the hint used list in Scoreboard table
def update_hint_used(game_id, team, question_number):
    dynamodb_client = boto3.client('dynamodb')

    # update the scoreboard item by appending the question number to the hint used list
    dynamodb_client.update_item(
        TableName='Scoreboard',
        Key={
            'game_id': {'S': game_id},
            'team': {'S': team}
        },
        UpdateExpression='ADD hint_used :question_number',
        ExpressionAttributeValues={
            ':question_number': {'NS': [str(question_number)]}
        }
    )


# broadcast the hint to the whole team
def broadcast_to_team(game_id, team, hint_message):
    # get all team participants in the game
    team_participants_connections = get_connections_for_game_and_team(game_id, team)
    print("team_participants_connections", team_participants_connections)

    # loop and send message to all team member's connection
    for connection in team_participants_connections:
        connection_id = connection['connection_id']
        print(connection_id)
        try:
            api_gateway_management_api.post_to_connection(ConnectionId=connection_id, Data=hint_message)
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

