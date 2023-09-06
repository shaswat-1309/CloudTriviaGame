import os
import csv
import boto3
import json
from google.cloud import storage
from io import StringIO

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Lambda function
def lambda_handler(event, context):
    
    # Load GCP key from environment variable 
    gcp_key = os.environ['GCP_KEY']
    
    # specify dynamodb table 
    table_name = 'Scoreboard'
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response['Items']

    # Extract field headers from the first item in the response
    field_headers = list(items[0].keys())

    # Load GCP credentials from the provided key file
    with open(gcp_key) as f:
        gcs_credentials = json.load(f)

    # Initialize GCP Storage client
    storage_client = storage.Client.from_service_account_info(gcs_credentials)

    # Convert items to CSV format
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)

    # Write data rows to the CSV file
    csv_writer.writerow(field_headers)

    for item in items:
        csv_writer.writerow(item.values())

    # Upload CSV data to Google Cloud Storage
    bucket_name = 'serverless-leaderboard'
    object_name = 'exported_data.csv'
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(csv_data.getvalue(), content_type='text/csv')

    # Return success response
    return {
        'statusCode': 200,
        'body': 'CSV export and upload to GCS successful'
    }
