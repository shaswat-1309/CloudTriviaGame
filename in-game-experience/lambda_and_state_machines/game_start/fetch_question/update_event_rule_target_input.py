import json
import boto3


def lambda_handler(event, context):
    print(event)
    game_id = event['game_id']

    # get lambda function (target) details
    lambda_function_name = 'fetch_question'
    lambda_client = boto3.client('lambda')
    lambda_function_arn = lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['FunctionArn']

    print(lambda_function_arn)

    rule_name = f'Game-{game_id}-Rule'

    # updated question number is already present in the event
    # (updated in the previous step/state of the FetchQuestion workflow)
    lambda_input_event = json.dumps(event)

    print(lambda_input_event)

    events_client = boto3.client('events')

    # update the event rule for the name by passing the updated input event with
    # the next question number updated so that the next invocation of the workflow displays the next question
    put_targets_response = events_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': lambda_function_arn,
                'Input': lambda_input_event
            }
        ]
    )

    print("put_targets_response", put_targets_response)

    return event
