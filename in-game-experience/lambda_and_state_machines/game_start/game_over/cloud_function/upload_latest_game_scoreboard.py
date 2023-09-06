import functions_framework
import csv
import io
from google.cloud import storage


# cloud function to update the latest game insights as CSV file to Cloud Storage,
# Looker studio report is configured with this cloud storage object as the data source
# in order to show the game insights after each game
@functions_framework.http
def update_game_insights(request):
    request_json = request.get_json(silent=True)
    print("request_json", request_json)

    if request_json:
        # extract game and team score details from the request
        game_id = request_json['game_id']
        team_scores = request_json['team_scores']

        # construct the bucket name and object name
        gcs_bucket_name = 'trivia-bucket'
        gcs_file_name = 'Scoreboard-data.csv'

        # preparing the CSV file headers
        csv_data = io.StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['game_id', 'team', 'score'])

        # preparing the CSV file content
        for team_data in team_scores:
            team_name = team_data.get('team', '')
            score = team_data.get('score', 0)
            csv_writer.writerow([game_id, team_name, score])

        print("csv data:", csv_data.getvalue())

        # get the cloud storage client, bucket and upload the constructed CSV file to the bucket
        gcs_client = storage.Client()
        print(gcs_client)
        bucket = gcs_client.bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_file_name)
        upload_response = blob.upload_from_string(csv_data.getvalue(), content_type='text/csv')

        print(upload_response)

        return {
            'statusCode': 200,
            'body': 'Successfully updated the csv'
        }

    else:
        return {
            'statusCode': 400,
            'body': 'Invalid input'
        }
