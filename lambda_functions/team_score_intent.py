import os
# TODO requires layer for requests
import requests


def fetch_score(team_name):
    request_json = {
        'team_name': team_name
    }
    get_team_score_url = os.environ['TEAM_SCORE_URL']
    get_team_score_response = requests.post(get_team_score_url, json=request_json)

    print("get_team_score_response:", get_team_score_response)

    if get_team_score_response.status_code == 200:
        team_score_details = get_team_score_response.json()
        return team_score_details
    else:
        score_details = {
            "error": "Error fetching team score!"
        }
        return score_details


def lambda_handler(event, context):
    # TODO implement
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    print("bot", bot)
    print("slots", slots)
    print("intent", intent)

    invocation_source = event['invocationSource']
    print("invocation_source", invocation_source)

    if invocation_source == 'DialogCodeHook':

        team_name_slot = slots['TeamName']

        print("team_name_slot", team_name_slot)

        if team_name_slot == None:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": "TeamName",
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                        "state": "Fulfilled"
                    }
                }
            }

        else:

            team_name = slots['TeamName']['value']['originalValue']

            score_data = fetch_score(team_name)
            if 'error' in score_data:
                print("Error")
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Close"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots,
                            "state": "Failed"
                        }

                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "The team score for " + team_name + " could not be fetched"
                        }
                    ]
                }

            else:
                # print("Success", score_data)
                score = score_data['Score']

                response = {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Close"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots,
                            "state": "Fulfilled"
                        }

                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "The team score for " + team_name + " is: " + str(score)
                        }
                    ]
                }

    print(response)

    return response