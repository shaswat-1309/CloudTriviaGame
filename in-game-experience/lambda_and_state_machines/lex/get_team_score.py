import json
import boto3


# lambda function to get the team score using team name
def lambda_handler(event, context):
    print(event)

    request_json = json.loads(event['body'])

    # get the team name from request
    team_name = request_json['team_name']

    # fetch the team score from DynamoDB table
    team_score_details = fetch_score(team_name)
    print(team_score_details)

    # return the team score details
    return {
        'statusCode': 200,
        "body": json.dumps(team_score_details)
    }


# fetch the team score from Teams table by filtering using team name
def fetch_score(team_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Teams')

    # get the item corresponding to the team name
    response = table.get_item(Key={
        "teamName": team_name
    })

    print(response)

    score_details = {}
    if 'Item' in response:
        # get the score from the get_item() response
        item = response['Item']
        score_details = {
            "TeamName": item['teamName'],
            "Score": str(item["teamScore"])
        }
    else:
        # return the error message if the query returned 0 elements
        score_details = {
            "error": "Team does not exist!"
        }
    return score_details
