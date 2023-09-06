import boto3
import json

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Lambda function
def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        team_name = body['team_name']
        
        # # Validate user ID against team player IDs
        # if not validate_user(user_id, team_name):
        #     response = {
        #         'statusCode': 400,
        #         'body': json.dumps({'error': 'Invalid User ID or Team Name'})
        #     }
        #     return response
        
        # Fetch upcoming games
        games = fetch_upcoming_games()
        
        # Return list of upcoming games
        response = {
            'statusCode': 200,
            'body': json.dumps(games)
        }
        return response
    
    except Exception as e:
        print(e)
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
        return response

# Function to validate if a user belongs to a team
def validate_user(user_id, team_name):
    teams_table = dynamodb.Table('Teams')
    response = teams_table.get_item(
        Key={'teamName': team_name}
    )
    if 'Item' in response:
        team = response['Item']
        player_ids = team.get('playerId', [])
        return user_id in player_ids
    return False

# Function to fetch upcoming games from the DynamoDB table
def fetch_upcoming_games():
    games_table = dynamodb.Table('quiz_game_table')
    response = games_table.scan(
        FilterExpression='#s = :status',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':status': 'Upcoming'}
    )
    games = response['Items']
    formatted_games = []
    for game in games:
        formatted_game = {
            'game_id': game['game_id'],
            'difficulty': game['difficulty'],
            'category': game['category'],
            'start_time': game['start_time'],
            'status': game['status'],
        }
        formatted_games.append(formatted_game)
    return formatted_games
