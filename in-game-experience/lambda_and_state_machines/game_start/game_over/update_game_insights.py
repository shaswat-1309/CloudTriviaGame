import json
import requests
import os


def lambda_handler(event, context):
    print(event)

    # the cloud function URL is extracted from the environment variable
    game_insights_url = os.environ['GAME_INSIGHTS_URL']
    admin_insights_url = os.environ['ADMIN_INSIGHTS_URL']

    try:

        # call the cloud function to update the game insights to be displayed using Looker studio
        game_insights_response = requests.post(game_insights_url, json=event)
        admin_insights_response = requests.post(admin_insights_url, json=event)

        print("game_insights_response:", game_insights_response)
        print("admin_insights_response:", admin_insights_response)
        # get the response
        if game_insights_response.status_code == 200:
            response = game_insights_response.json()
        else:
            print(f"API call failed with status code: {game_insights_response.status_code}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

    return event
