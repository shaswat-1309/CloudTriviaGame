import json
import os

import boto3
import datetime


def lambda_handler(event, context):
    print(event)

    # get the game start time in UTC
    start_time_str = event['start_time']
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%SZ')

    # get the current time in UTC
    current_time = datetime.datetime.utcnow()

    # compare the current time with the game start time
    if current_time < start_time:

        # show error message if being triggered before the start time
        return {
            'statusCode': 200,
            'body': 'Triggered before game start time'
        }

    else:
        fetch_question_step_fn_arn = os.environ['FETCH_QN_STEP_FN_ARN']
        # call the step function to broadcast questions, answers, live scores to the frontend
        stepfunctions = boto3.client('stepfunctions')
        response = stepfunctions.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:182296130665:stateMachine:FetchQuestion',
            input=json.dumps(event)
        )

        print(response)

        return {
            'statusCode': 200,
            'body': 'Step Functions workflow started successfully.'
        }
