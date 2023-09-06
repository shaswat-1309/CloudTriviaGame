import boto3
import json
import datetime

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
participants_table = dynamodb.Table('Participants')
games_table = dynamodb.Table('quiz_game_table')

# Lambda function
def lambda_handler(event, context):
    
    request_body = json.loads(event['body'])
    user_id = request_body['user_id']
    team_name = request_body['team_name']
    game_id = request_body['game_id']

    users_joined = []
    
    # Check if the user has already joined
    existing_entry = participants_table.get_item(Key={'game_id': game_id}).get('Item', None)
    
    if existing_entry:
        participants = existing_entry.get('participants', [])
        for entry in participants:
            if user_id in entry.get('usersJoined', []):
                users_joined = entry.get('usersJoined', [])
                game_details = games_table.get_item(Key={'game_id': game_id})['Item']
                category = game_details['category']
                difficulty = game_details['difficulty']
                start_time_str = game_details['start_time']
                status = game_details['status']
                total_users_joined = sum(len(team.get('usersJoined', [])) for team in participants)

                response_data = {
                    'game_id': game_id,
                    'category': category,
                    'difficulty': difficulty,
                    'start_time': start_time_str,
                    'status': status,
                    'user_id': user_id,
                    'team_name': team_name,
                    'participant_count': total_users_joined,
                    'users_joined': users_joined,
                    'message': 'User has already joined the game.'
                }
            
                response = {
                    'statusCode': 200,
                    'body': json.dumps(response_data)
                }
                return response

    # Retrieve the existing game_id entry from the Participants table
    game_entry = participants_table.get_item(Key={'game_id': game_id}).get('Item', None)

    users_joined = []
    participants = []

    if game_entry:
        # Game exists, check if the team_name exists in the participants
        participants = game_entry.get('participants', [])
        for entry in participants:
            if entry['team_name'] == team_name:
                # Team exists, append user_id to the existing team entry
                users_joined = entry.get('usersJoined', [])
                users_joined.append(user_id)
                break
        else:
            # Team doesn't exist, create a new team entry
            participants.append({'team_name': team_name, 'usersJoined': [user_id]})

        # Update the existing entry with the updated participants list
        participants_table.update_item(
            Key={'game_id': game_id},
            UpdateExpression='SET participants = :p',
            ExpressionAttributeValues={':p': participants}
        )
    else:
        # Game doesn't exist, create a new entry with the participant details
        participants_table.put_item(
            Item={
                'game_id': game_id,
                'participants': [{'team_name': team_name, 'usersJoined': [user_id]}]
            }
        )

    # Retrieve game details
    game_details = games_table.get_item(Key={'game_id': game_id})['Item']
    category = game_details['category']
    difficulty = game_details['difficulty']

    # Convert the 'start_time' string to a datetime object
    start_time_str = game_details['start_time']

    status = game_details['status']

    # Calculate the total number of users joined across all teams
    total_users_joined = sum(len(team.get('usersJoined', [])) for team in participants)

    response_data = {
        'game_id': game_id,
        'category': category,
        'difficulty': difficulty,
        'start_time': start_time_str,  
        'status': status,
        'user_id': user_id,
        'team_name': team_name,
        'participant_count': total_users_joined,
        'users_joined': users_joined
    }

    # return game details and waiting room details
    response = {
        'statusCode': 200,
        'body': json.dumps(response_data)
    }
    return response

