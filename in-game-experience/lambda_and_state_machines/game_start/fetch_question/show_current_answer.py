import boto3
import json
import os


# apigatewaymanagementapi client by passing websocket url to broadcast the message to open connections
apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ['ENDPOINT_URL'])


def lambda_handler(event, context):
    print("orig event", event)

    game_id = event['game_id']

    # calculate prev question no. since previous question's answer has to be displayed
    question_number = event["question_number"] - 1

    print(f"fetching ans for {question_number} event")

    #  get all participants connection for the current game
    game_participants_response = get_game_participants(game_id)
    print('game_participants_response', game_participants_response)

    # get the answer to the question, in order to display in the frontend
    answer_details = get_answer_details(game_id, question_number)

    # get the live team score after each question time is completed, in order to display in the frontend
    team_scores = get_score_details(game_id)

    # construct the broadcast message including answer details and team scores
    broadcast_message = {
        "answer_details": answer_details,
        "team_scores": team_scores
    }
    print('broadcast_message', broadcast_message)

    broadcast_message_str = json.dumps(broadcast_message)

    # loop through each connection and broadcast the message to each participant connection
    for item in game_participants_response['Items']:
        connection_id = item['connection_id']
        send_message_to_connection(connection_id, broadcast_message_str)

    # put the team score details in the event in order to show when showing questions
    event['team_scores'] = team_scores
    return event


def get_answer_details(game_id, question_number):
    answer_details = {}

    game_questions_table = 'GameQuestions'
    dynamodb_client = boto3.client('dynamodb', region_name=os.environ['REGION'])

    try:
        # fetch the answer details (correct answer, explanation) from the GameQuestions table
        response = dynamodb_client.get_item(
            TableName=game_questions_table,
            Key={
                'game_id': {'S': game_id},
                'question_number': {'N': str(question_number)}
            }
        )

        question = response.get('Item', {})
        question_text = question.get('question', {}).get('S', '')
        options = [option.get('S', '') for option in question.get('options', {}).get('L', [])]
        correct_option_index = int(question.get('correct_option', {}).get('N', '0'))
        correct_option = options[correct_option_index]
        explanation = question.get('explanation', {}).get('S', '')

        # return the correct answer, explanation, and team scores as a JSON response
        answer_details = {
            'question': question_text,
            'options': options,
            'correct_option': correct_option,
            'explanation': explanation
        }

    except Exception as e:
        print(f"Exception occurred - {e}")

    return answer_details


def get_score_details(game_id):

    team_scores = []

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Scoreboard')

    # query to get the result ordered by score field using the game_id score index created on the Scoreboard table
    response = table.query(
        IndexName='GameScoreIndex',
        KeyConditionExpression='game_id = :game_id',
        ExpressionAttributeValues={
            ':game_id': game_id
        },
        ScanIndexForward=False  # for getting score in descending order
    )

    # Get the items (team scores) from the response
    items = response['Items']
    print("get_score_details", items)

    # construct the scores for all teams as a list
    for item in items:
        team_score = {
            "team": item['team'],
            "score": int(item['score'])
        }
        team_scores.append(team_score)

    return team_scores


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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GameParticipants')  # Replace with your table name
    response = table.query(
        KeyConditionExpression='game_id = :game_id',
        ExpressionAttributeValues={':game_id': game_id}
    )
    print(response)
    return response


