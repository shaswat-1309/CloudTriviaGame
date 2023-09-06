import boto3
from collections import defaultdict
from datetime import datetime, timedelta
import json
from decimal import Decimal

# Initialize the AWS SNS client
sns = boto3.client('sns')

# JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
    
# Specify score leaderboard table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Scoreboard')

# Function to send email to highest scoring team
def send_email_to_team(team_name, category, highest_score):
    if category:
        subject = f"Congratulations, {team_name}! You are the highest scorer in {category} category!"
        message=f"Congratulations, {team_name}! You have achieved the highest score of {highest_score} in {category} category on leaderboard."
    else:
        subject = f"Congratulations, {team_name}! You have scored highest on global leaderboard!"
        message=f"Congratulations, {team_name}! You have achieved the highest score of {highest_score} on the leaderboard."
    
    # change team name string format (replace space with underscore)
    team_topic = team_name.replace(" ", "_")

    # replace with sreedevi's account arn
    topic_arn = f"arn:aws:sns:us-east-1:115789338221:{team_topic}"
    sns.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message
    )

# Function to filter time frame
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

# Function to get all unique category list
def get_categories():
    response = table.scan(ProjectionExpression='category')
    categories_data = response['Items']
    categories = set(category['category'] for category in categories_data)
    return list(categories)

# Lambda function
def lambda_handler(event, context):
    is_periodic_trigger=False
    
    # Check if the Lambda is triggered by CloudWatch Events or API call
    if "source" in event:
        if event['source'] == 'aws.events':
            is_periodic_trigger=True
            
    # Extract query parameters
    time_frame = event.get('queryStringParameters', {}).get('time_frame', 'all time')
    category = event.get('queryStringParameters', {}).get('category')

    start_time_filter = get_start_time_filter(time_frame)

    # Fetch the list of categories
    categories = get_categories()

    response = table.scan()
    leaderboard_data = response['Items']

    # Filter leaderboard data by category if a category is specified
    if category:
        leaderboard_data = [entry for entry in leaderboard_data if entry['category'] == category]

    # Calculate global scores for each team_name based on the filtered time frame
    global_scores = defaultdict(int)
    for entry in leaderboard_data:
        start_time = entry['start_time']
        if not start_time_filter or datetime.fromisoformat(start_time) >= start_time_filter:
            team_name = entry['team']
            score = entry['score']
            global_scores[team_name] += score

    # Final result with team_name and their scores
    leaderboard_result = []
    for team_name, score in global_scores.items():
        leaderboard_result.append({
            'team_name': team_name,
            'score': score
        })

    # Sort leaderboard data in descending order of scores
    leaderboard_result.sort(key=lambda entry: entry['score'], reverse=True)

    # Find the team with the highest score
    highest_score_entry = leaderboard_result[0]
    highest_score_team_name = highest_score_entry['team_name']
    highest_score = highest_score_entry['score']
    
    if is_periodic_trigger:
        # Send email to the team with the highest score
        send_email_to_team(highest_score_team_name, category, highest_score)

    # Return the response with list of categories and leaderboard data
    return {
        'statusCode': 200,
        'body': json.dumps({
            'categories': categories,
            'leaderboard': leaderboard_result
        }, cls=DecimalEncoder)
    }
