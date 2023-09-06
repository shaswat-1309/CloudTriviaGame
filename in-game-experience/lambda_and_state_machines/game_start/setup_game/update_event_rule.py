import json
import boto3
import os


def lambda_handler(event, context):
    print(event)
    game_id = event['game_id']

    # construct game rule name
    rule_name = f'Game-{game_id}-Rule'

    # trigger fetch question related lambda/step function every 1 min
    # to display question in this interval, 45 sec for each question and
    # 15 sec in between to display the answer
    schedule_expression = 'rate(1 minute)'

    # update the game event rule
    rule_arn = update_event_rule_schedule(rule_name, schedule_expression)

    # update the target lambda function from setup_game to fetch_question
    lambda_function_name = "fetch_question"
    lambda_input_event = json.dumps(event)
    update_event_rule_target(rule_arn, rule_name, lambda_function_name, lambda_input_event)

    return event


# update the game event rule
def update_event_rule_schedule(rule_name, schedule_expression):
    events_client = boto3.client('events')

    response = events_client.put_rule(
        Name=rule_name,
        ScheduleExpression=schedule_expression
    )

    print("update_event_rule_schedule", response)

    return response['RuleArn']


# update the target lambda to fetch_question
def update_event_rule_target(rule_arn, rule_name, lambda_function_name, lambda_input_event):

    lambda_client = boto3.client('lambda')
    lambda_function_arn = lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['FunctionArn']

    events_client = boto3.client('events')
    response = events_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': lambda_function_arn,
                'Input': lambda_input_event
            }
        ]
    )

    print("update_event_rule_target", response)

    configure_lambda_resource_policy(lambda_function_name, rule_name, rule_arn)


# add permission for lambda to be invoked by eventbridge
def configure_lambda_resource_policy(lambda_function_name, rule_name, rule_arn):
    lambda_client = boto3.client('lambda', region_name=os.environ['REGION'])

    try:
        response = lambda_client.add_permission(
            FunctionName=lambda_function_name,
            StatementId=f'EventBridgeInvokePermission_{rule_name}_{lambda_function_name}',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=rule_arn
        )
        print("configure_lambda_resource_policy", response)
        print(f"Resource-based policy configured for Lambda function: {lambda_function_name}")

    except Exception as e:
        print("Exception occurred!", e)
