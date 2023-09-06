from google.cloud import firestore
from flask import make_response

db = firestore.Client()

def deletequestion(request):
    try:
        # Handle preflight request for CORS
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
            return response

        # Handle the actual DELETE request
        if request.method == 'POST':
            # Retrieve the question ID from the request JSON payload
            request_json = request.get_json()
            document_id = request_json['document_id']

            # Delete the question document from Firestore
            doc_ref = db.collection('questions').document(document_id)
            doc_ref.delete()

            # Return a success response
            response_data = 'Question deleted successfully'
            response = make_response(response_data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')

            return response

        # Handle other methods (if needed)
        else:
            return ('Method not allowed', 405)

    except Exception as e:
        response_data = f"Error occurred: {e}"
        response = make_response(response_data, 500)
        return response
