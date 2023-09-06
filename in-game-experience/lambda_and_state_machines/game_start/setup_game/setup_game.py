import json
import boto3
import os


def lambda_handler(event, context):
    print(event)

    # get setup game step fn arn from environment variable
    setup_game_step_fn_arn = os.environ['SETUP_GAME_STEP_FN_ARN']

    stepfunctions = boto3.client('stepfunctions')

    # start the setup game workflow
    response = stepfunctions.start_execution(
        stateMachineArn=setup_game_step_fn_arn,
        input=json.dumps(event)
    )

    print(response)
