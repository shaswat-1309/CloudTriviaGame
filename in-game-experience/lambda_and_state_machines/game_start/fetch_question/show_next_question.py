import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GameParticipants')

# apigatewaymanagementapi client by passing websocket url to broadcast the message to open connections
apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', endpoint_url=os.environ['ENDPOINT_URL'])


def lambda_handler(event, context):
    game_id = event['game_id']
    next_question_number = event['question_number']

    try:
        # Fetch all connections from the GameParticipants table
        game_participants_response = get_game_participants(game_id)

        print('game_participants_response', game_participants_response)

        # fetch the next question to be displayed
        question_details = fetch_question(game_id, next_question_number)
        print('question_details', question_details)
        question_details_str = json.dumps(question_details)

        # loop through each connection and display the question
        for item in game_participants_response['Items']:
            print(item)
            connection_id = item['connection_id']
            send_message_to_connection(connection_id, question_details_str)

        # increment the question_number by one for next round
        event['question_number'] += 1

        # check and set the last question flag to stop the workflow
        if event["question_number"] > event["no_of_questions"]:
            event['is_last_question'] = True

        print("updated event", event)

        return event

    except Exception as e:
        print('Error broadcasting message:', e)
        return event


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
    response = table.query(
        KeyConditionExpression='game_id = :game_id',
        ExpressionAttributeValues={':game_id': game_id}
    )
    print(response)
    return response


# fetch  next question from the GameQuestions table
def fetch_question(game_id, next_question_number):
    dynamodb_client = boto3.client('dynamodb', region_name=os.environ['REGION'])

    table_name = 'GameQuestions'

    try:
        # fetch the question from the GameQuestions DynamoDB table
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={
                'game_id': {'S': game_id},
                'question_number': {'N': str(next_question_number)}
            }
        )

        # extract the question details from the response
        # TODO REMOVE CORRECT ANS HINT EXPLANATION FROM THIS
        question = response.get('Item', {})
        question_details = {
            'question': question.get('question', {}).get('S', ''),
            'options': [option.get('S', '') for option in question.get('options', {}).get('L', [])],
            'correct_option': int(question.get('correct_option', {}).get('N', '0')),
            'hint': question.get('hint', {}).get('S', ''),
            'explanation': question.get('explanation', {}).get('S', ''),
            'question_number': int(question.get('question_number', {}).get('N', ''))
        }

        # return the question details as a JSON response
        return question_details

    except Exception as e:
        return {
            'error': "question could not be fetched"
        }

