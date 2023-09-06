import json
import boto3


def lambda_handler(event, context):
    print(event)
    game_id = event['game_id']

    rule_name = f'Game-{game_id}-Rule'
    eventbridge_client = boto3.client('events')

    try:
        # disable the event rule for the game after the game ends
        response = eventbridge_client.disable_rule(Name=rule_name)

        print(response)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f"The rule '{rule_name}' has been disabled.")
        else:
            print(f"Failed to disable the rule '{rule_name}'.")

    except Exception as e:
        return f"Error disabling the rule '{rule_name}': {str(e)}"

    return event