import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GameParticipants')


# participant exits game from the UI exit game button
def lambda_handler(event, context):
    print(event)
    try:
        # extract the connectionId and other details from the request event
        connection_id = event['requestContext']['connectionId']
        disconnect_reason = event['requestContext']['disconnectReason']

        # parse the event data to get the gameId
        disconnect_event_data = json.loads(disconnect_reason)
        game_id = disconnect_event_data.get('gameId', None)

        print(game_id)

        # delete the participant connection from the GameParticipants using game_id and connection d
        if game_id:
            table.delete_item(Key={
                'game_id': game_id,
                'connection_id': connection_id
            })

        return {
            'statusCode': 200,
            'body': 'Connection details removed successfully.',
        }

    except Exception as e:
        print('Error removing connection details:', e)
        return {
            'statusCode': 500,
            'body': 'Error removing connection details.',
        }
