import json
import boto3
from datetime import datetime


def lambda_handler(event, context):
    print(event)
    # parse the WebSocket connection request event to get the connection id
    connection_id = event['requestContext']['connectionId']

    # get the query string params containing game, team and user details
    query_params = event.get('queryStringParameters')

    if query_params is None:
        return {
            'statusCode': 400,
            'body': 'Missing game,team and user details in the WebSocket connection request'
        }

    # extract the game, team and user details
    game_id = query_params['gameId']
    team = query_params['teamName']
    user_id = query_params['userId']
    category = query_params['category']
    start_time = query_params['start_time']

    # add the connection info to participants table
    add_participant_response = add_game_participants(connection_id, game_id, team, user_id)

    if add_participant_response:

        # make Scoreboard entry for team when the first participant joins
        add_team_to_scoreboard(game_id, team, category, start_time)

        return {
            'statusCode': 200,
            'body': 'Successfully stored connection details'
        }

    else:

        return {
            'statusCode': 500,
            'body': 'Error storing connection details'
        }


# adding the participant to table
def add_game_participants(connection_id, game_id, team, user_id):
    # Store the connection details in the GameParticipants table
    try:
        item = {
            'connection_id': connection_id,
            'game_id': game_id,
            'team': team,
            'user_id': user_id
        }

        dynamodb = boto3.resource('dynamodb')
        table_name = 'GameParticipants'
        table = dynamodb.Table(table_name)

        response = table.put_item(Item=item)
        print("Item successfully added:", response)
        return True

    except Exception as e:
        print("Error storing connection details:", e)
        return False


def add_team_to_scoreboard(game_id, team_name, category, start_time):
    dynamodb = boto3.client('dynamodb')

    # TODO START TIME AND CATEGORY

    # convert to datetime object to format supported by Leaderboard
    datetime_object = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')

    # Format the datetime object to the desired format
    formatted_time = datetime_object.strftime('%Y-%m-%dT%H:%M')

    item = {
        'game_id': {'S': game_id},
        'team': {'S': team_name},
        'score': {'N': str(0)},
        'responses': {'M': {}},
        'start_time': {'S': formatted_time},
        'category': {'S': category}
    }

    # game id team id combination check
    condition_expression = 'attribute_not_exists(game_id) AND attribute_not_exists(team)'

    try:
        # Add the item to the table if the game id and team id combination entry does not exist
        response = dynamodb.put_item(
            TableName='Scoreboard',
            Item=item,
            ConditionExpression=condition_expression
        )

        print(response)
        print(f"Scoreboard entry game - {game_id} and team - {team_name} added successfully")

    except Exception as e:
        print(e)
        print(f"Scoreboard entry game - {game_id} and team - {team_name} was not added")

