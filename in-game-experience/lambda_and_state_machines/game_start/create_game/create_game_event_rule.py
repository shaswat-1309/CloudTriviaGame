# tested

import boto3
from datetime import datetime, timedelta
from dateutil import tz
import json
import os


def lambda_handler(event, context):
    print(event)

    # extract the required game information from the event
    game_id = event['game_id']
    game_name = event['game_name']
    no_of_questions = event['no_of_questions']
    category = event['category']
    difficulty = event['difficulty']

    game_start_time_str = event['start_time']
    game_start_time = datetime.strptime(game_start_time_str, '%Y-%m-%dT%H:%M:%SZ')

    # schedule the event bridge rule to call the setup game functionalities x minutes before the game starts
    game_setup_time = game_start_time - timedelta(minutes=2)

    # create the event input to be passed to the lambda function invoked by event rule
    lambda_input_event = json.dumps({
        "game_id": game_id,
        "game_name": game_name,
        "no_of_questions": no_of_questions,
        "category": category,
        "difficulty": difficulty,
        "question_number": 1,
        "start_time": game_start_time_str
    })

    # create the EventBridge rule for the game
    rule_name = f'Game-{game_id}-Rule'
    create_event_bridge_rule(rule_name, game_setup_time, lambda_input_event, game_id)

    return {
        'statusCode': 200,
        'body': f'EventBridge rule {rule_name} created successfully'
    }


def create_event_bridge_rule(rule_name, start_time, lambda_input_event, game_id):
    print("create_event_bridge_rule")
    events_client = boto3.client('events')

    # create the EventBridge rule to trigger the setup_game lambda function x minutes before the game starts
    response = events_client.put_rule(
        Name=rule_name,
        ScheduleExpression=f'cron({start_time.minute} {start_time.hour} {start_time.day} {start_time.month} ? {start_time.year})',
        State='ENABLED',
        Description='Trigger the Lambda function at a specific time'
    )
    rule_arn = response['RuleArn']

    # set the target for the rule as setup_game lambda function, pass the lambda event input
    lambda_client = boto3.client('lambda')
    lambda_function_name = 'setup_game'
    lambda_function_arn = lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['FunctionArn']

    events_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': lambda_function_arn,
                'Input': lambda_input_event
            }
        ]
    )
    configure_lambda_resource_policy(lambda_function_name, rule_arn, game_id)


def configure_lambda_resource_policy(lambda_function_name, rule_arn, game_id):
    lambda_client = boto3.client('lambda', region_name=os.environ['REGION'])

    # add the resource-based policy to the Lambda function to be invoked by event rule
    response = lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId=f'EventBridgeInvokePermission_{game_id}',
        Action='lambda:InvokeFunction',
        Principal='events.amazonaws.com',
        SourceArn=rule_arn
    )
    print(response)
    print(f"Resource-based policy configured for Lambda function: {lambda_function_name}")

