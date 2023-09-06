import boto3
import json


dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    print(event)
    event_body = json.loads(event['body'])

    # extract answer from submit request
    submitted_response = event_body['answerDetails']

    print("submitted response:", submitted_response)

    # extract game, team, user, question number, chosen option from the request
    game_id = submitted_response['gameId']
    team = submitted_response['teamName']
    user_id = submitted_response['userId']
    question_number = submitted_response['questionNumber']
    chosen_option = submitted_response['chosenOption']

    try:
        # check if answer is already submitted by the team
        is_already_submitted = check_if_already_submitted(game_id, team, question_number)

        # if yes, don't update the DB
        if is_already_submitted:
            print("Response already recorded!")
            # return a response saying answer is already submitted
            return {
                'statusCode': 200,
                'body': json.dumps('Response already recorded!')
            }

        # else, get the correct answer and save the submitted answer and calculate score for the team
        else:
            # get the correct answer of the question
            correct_answer = get_answer_to_question(game_id, question_number)

            # determine the score to be added
            score = 10 if correct_answer is not None and chosen_option == int(correct_answer) else 0

            # prepare the response dictionary as a JSON string
            response_data = {
                'user': user_id,
                'chosen_option': chosen_option
            }
            response_json = json.dumps(response_data)

            # save the submitted answer and score for the current submission
            save_submitted_answer_and_score(game_id, team, question_number, score, response_json)

            # Return a successful response
            return {
                'statusCode': 200,
                'body': json.dumps('Answer submitted successfully.')
            }

    except Exception as e:
        print('Error submitting answer:', e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error submitting answer!')
        }


# check if the answer to the question has already been submitted
def check_if_already_submitted(game_id, team, question_number):

    # fetch the current responses field for the specific team
    response = dynamodb_client.get_item(
        TableName='Scoreboard',
        Key={
            'game_id': {'S': game_id},
            'team': {'S': team}
        },
        ProjectionExpression='responses'
    )

    # get the current responses map for the team
    responses_map = response.get('Item', {}).get('responses', {}).get('M', {})

    print("existing team responses: ", responses_map)

    if str(question_number) not in responses_map:
        return False

    else:
        return True


# get the correct answer of the question
def get_answer_to_question(game_id, question_number):
    # get the correct_option from the game_questions table
    correct_option_response = dynamodb_client.get_item(
        TableName='GameQuestions',
        Key={
            'game_id': {'S': game_id},
            'question_number': {'N': str(question_number)}
        },
        ProjectionExpression='correct_option'
    )
    return correct_option_response.get('Item', {}).get('correct_option').get('N', None)


# save the submitted answer and score for the current submission
def save_submitted_answer_and_score(game_id, team, question_number, score, submitted_response):
    # update the responses field and the score in the scoreboard item
    dynamodb_client.update_item(
        TableName='Scoreboard',
        Key={
            'game_id': {'S': game_id},
            'team': {'S': team}
        },
        UpdateExpression=f'SET responses.#question_number = :response ADD score :score',
        ExpressionAttributeNames={
            '#question_number': str(question_number)
        },
        ExpressionAttributeValues={
            ':response': {'S': submitted_response},
            ':score': {'N': str(score)}
        }
    )
    print("Response has been successfully recorded!")

