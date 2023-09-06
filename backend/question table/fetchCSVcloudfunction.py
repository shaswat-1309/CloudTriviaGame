import os
import csv
import boto3
from google.cloud import storage
from dotenv import load_dotenv
from flask import escape

def fetchCSV(request):
    # Handle preflight (OPTIONS) request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',  # Replace * with the allowed origin(s) for security
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Handle actual (POST) request
    if request.method == 'POST':
        data = []  # Initialize the data list before the try-except block
        headers = ['game_id', 'team', 'score']  # Replace with your table headers
        try:
            load_dotenv()
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            aws_session_token = os.getenv('AWS_SESSION_TOKEN')
            aws_region = os.getenv('AWS_REGION')

            # Replace 'YourDynamoDBTableName' with the actual name of your DynamoDB table
            table_name = 'Scoreboard'
            # Replace 'your-gcs-bucket-name' with the name of your Google Cloud Storage bucket
            bucket_name = 'tada_b0088888'
            # Replace 'your-output-file.csv' with the desired name of the CSV file in Cloud Storage
            output_file_name = 'adminReportFile.csv'

            dynamodb = boto3.client('dynamodb',
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key,
                                    aws_session_token=aws_session_token,
                                    region_name=aws_region)

            # Query the table to fetch data (modify the parameters based on your query requirements)
            response = dynamodb.scan(TableName=table_name)

            # Extract relevant data from the DynamoDB response (modify based on your table structure)
            for item in response['Items']:
                # Assuming the items in DynamoDB are in the format {"attribute_name": {"S": "value"}}
                game_id = item['game_id']['S']
                team = item['team']['S']  # Assuming no_of_questions is a number (N) type
                score = item['score']['N']

                # Append the attributes to the data list as a row in the CSV
                data.append([game_id, team, score])

            # Insert the headers as the first row in the data list
            data.insert(0, headers)

            # Convert data to CSV and write to a temporary file
            temp_csv_path = '/tmp/temp_data.csv'
            with open(temp_csv_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(data)

            # Upload the CSV file to Google Cloud Storage
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(output_file_name)
            blob.upload_from_filename(temp_csv_path)

            # Delete the temporary file
            os.remove(temp_csv_path)

            # Set CORS headers for the response
            headers = {
                'Access-Control-Allow-Origin': '*',  # Replace * with the allowed origin(s) for security
            }

            return ('CSV file successfully uploaded to Google Cloud Storage!', 200, headers)

        except Exception as e:
            # Set CORS headers for the response
            headers = {
                'Access-Control-Allow-Origin': '*',  # Replace * with the allowed origin(s) for security
            }

            return (str(e), 500, headers)

    # Return an error for unsupported request methods
    return ('Method Not Allowed', 405, {'Allow': 'POST'})