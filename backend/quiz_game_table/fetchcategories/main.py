from google.cloud import firestore
from flask import jsonify, make_response

db = firestore.Client.from_service_account_json("serviceKey.json")

def fetchcategories(request):
    try:
        # Handle preflight request for CORS
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
            return response

        # Handle the actual GET request
        if request.method == 'GET':
            categories_ref = db.collection('categories')
            categories_docs = categories_ref.stream()

            categories = []
            for doc in categories_docs:
                category = doc.to_dict()
                category['id'] = doc.id
                categories.append(category)

            # Return the categories as JSON response
            response_data = jsonify(categories)
            response = make_response(response_data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')

            return response

        # Handle other methods (if needed)
        else:
            return ('Method not allowed', 405)

    except Exception as e:
        response_data = f"Error occurred: {e}"
        response = make_response(response_data, 500)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')

        return response
