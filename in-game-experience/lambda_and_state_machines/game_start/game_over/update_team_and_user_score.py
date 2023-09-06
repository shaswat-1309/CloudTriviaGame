import boto3
import os
import requests


def lambda_handler(event, context):
    game_id = event['game_id']
    team_scores = event['team_scores']

    dynamodb = boto3.client('dynamodb')

    user_scores = []
    # extract the team names and scores from the event and store in the Teams table
    for team_score in team_scores:
        print(team_score)

        team_name = team_score['team']

        # update the team table by adding the new score to existing team's score
        dynamodb.update_item(
            TableName='Teams',
            Key={
                'teamName': {'S': team_score['team']}
            },
            UpdateExpression='ADD teamScore :score',
            ExpressionAttributeValues={
                ':score': {'N': str(team_score['score'])}
            }
        )

        team_members_uuids = get_team_members(team_name)
        print("team_members_uuids:", team_members_uuids)
        team_member_score_pairs = update_team_members_score(team_members_uuids, team_score)
        user_scores += team_member_score_pairs

    update_user_scores(user_scores)

    return event


def update_user_scores(user_scores):
    update_user_score_url = os.environ['UPDATE_USER_SCORE_URL']

    email_score_pairs = {
        'emailScorePairs': user_scores
    }
    update_user_score_response = requests.post(update_user_score_url, json=email_score_pairs)

    print("update_user_score_response:", update_user_score_response)
    # get the response
    if update_user_score_response.status_code == 200:
        print("APIs called successfully")
    else:
        print(f"API call failed with status code: {update_user_score_response.status_code}")


def get_team_members(team_name):
    team_members = []
    dynamodb_client = boto3.client('dynamodb')

    response = dynamodb_client.get_item(
        TableName='Teams',
        Key={
            'TeamName': {'S': team_name}
        },
        ProjectionExpression='playerId'
    )
    # extract and return the hint used list value
    members = response['Item'].get('playerId', {'L': []})
    return members.get('L', [])  # TODO check if getting it correctly


def update_team_members_score(team_members, team_score):
    email_score_pair = []

    # extract the team names and scores from the event and store in the Teams table
    for member in team_members:
        member_score = {
            "email": member,
            "score": team_score
        }
        email_score_pair.append(member_score)

    return email_score_pair