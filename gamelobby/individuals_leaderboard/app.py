import boto3
from collections import defaultdict
from datetime import datetime, timedelta
import json
from decimal import Decimal

# JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
category_leaderboard_table = dynamodb.Table('Scoreboard')
teams_table = dynamodb.Table('Teams')

# Function for time frame filter 
def get_start_time_filter(time_frame):
    now = datetime.utcnow()
    if time_frame == 'daily':
        return now - timedelta(days=1)
    elif time_frame == 'weekly':
        return now - timedelta(weeks=1)
    elif time_frame == 'monthly':
        return now - timedelta(days=30)  
    else:  # For 'all time', return None to indicate no filter
        return None

# Function to get a list of unique categories from the leaderboard table
def get_categories():
    response = category_leaderboard_table.scan(ProjectionExpression='category')
    categories_data = response['Items']
    categories = set(category['category'] for category in categories_data)
    return list(categories)

# Function to calculate player scores for a specific category and time frame
def get_players_scores_for_category(category, start_time_filter):
    response = category_leaderboard_table.scan(FilterExpression='category = :category', ExpressionAttributeValues={':category': category})
    leaderboard_data = response['Items']

    # Calculate player scores for the category and filtered time frame
    player_scores = defaultdict(int)
    for entry in leaderboard_data:
        start_time = entry['start_time']
        if not start_time_filter or datetime.fromisoformat(start_time) >= start_time_filter:
            team_name = entry['team']
            score = entry['score']

            # Fetch the list of playerIds for the team
            team_response = teams_table.get_item(Key={'teamName': team_name})
            if 'Item' in team_response:
                player_ids = team_response['Item']['playerId']
                for player_id in player_ids:
                    player_scores[player_id] += score

    return player_scores

# Lambda function
def lambda_handler(event, context):

    # Extract query parameters from the event
    time_frame = event.get('queryStringParameters', {}).get('time_frame', 'all time')
    category = event.get('queryStringParameters', {}).get('category')

    # Calculate the start time filter based on the specified time frame
    start_time_filter = get_start_time_filter(time_frame)

    # Fetch the list of categories
    categories = get_categories()
    
    if category:
        # Calculate player scores for the category
        player_scores = get_players_scores_for_category(category, start_time_filter)
        player_leaderboard_result = [{'playerId': player_id, 'score': score} for player_id, score in player_scores.items()]
    else:
        # Calculate global player scores for all categories
        categories = get_categories()
        global_player_scores = defaultdict(int)
        for cat in categories:
            cat_scores = get_players_scores_for_category(cat, start_time_filter)
            for player_id, score in cat_scores.items():
                global_player_scores[player_id] += score

        player_leaderboard_result = [{'playerId': player_id, 'score': score} for player_id, score in global_player_scores.items()]

    # Sort player leaderboard data in descending order of scores
    player_leaderboard_result.sort(key=lambda entry: entry['score'], reverse=True)

    # Return the responses with category list and player leaderboard data
    return {
        'statusCode': 200,
        'body': json.dumps({
            'categories': categories,
            'leaderboard': player_leaderboard_result
        }, cls=DecimalEncoder)
    }
