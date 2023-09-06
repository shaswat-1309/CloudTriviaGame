from flask import jsonify, request
from google.cloud import firestore
from google.cloud import language_v1

# Initialize Firestore and Language API clients
db = firestore.Client.from_service_account_json("serviceKey.json")
language_client = language_v1.LanguageServiceClient.from_service_account_json("serviceKey.json")


def add_categories_to_collection(category):
    categories_collection = db.collection('categories')
    categories_document = categories_collection.document('categories')

    # Check if the document already exists
    if categories_document.get().exists:
        existing_categories = categories_document.get().to_dict().get('categories', [])
        if category not in existing_categories:
            existing_categories.append(category)
            categories_document.update({'categories': existing_categories})
    else:
        categories_document.set({'categories': [category]})


def determine_tags(text):
    try:
        # Use the Natural Language API to determine the tags (categories) of the question
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = language_client.classify_text(request={'document': document})

        # Get the tags (categories) with their confidence scores
        tags = response.categories

        # Extract unique tags (categories) from the response
        tag_set = set()
        for tag in tags:
            tag_name = tag.name
            tag_names = tag_name.split('/')
            for name in tag_names:
                if name:
                    tag_set.add(name)

        if tag_set:
            return list(tag_set)
    except Exception as e:
        print(f"Error occurred while determining tags (categories): {e}")
        return ['Miscellaneous']
    return ['Miscellaneous']  # Default tag (category) if an error occurs or no relevant tag is found

def addquestion(request):

    if request.method == "OPTIONS":
        # Allows POST requests from any origin with the Content-Type
        # header and caches preflight response for 3600 seconds
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    try:

        if request.method == 'POST':
            # Retrieve the question, options, correct option, difficulty, hint, explanation, and category from the request JSON payload
            request_json = request.get_json()
            print(request_json)
            question = request_json['question']
            options = request_json['options']
            correct_option = request_json['correct_option']
            difficulty = request_json['difficulty']
            hint = request_json['hint']
            explanation = request_json['explanation']
            category = request_json['category']  # New field for category

            # Determine the tags of the question using Natural Language API
            tags = determine_tags(question + ' ' + hint)

            # Create a new document in the 'questions' collection
            doc_ref = db.collection('questions').document()

            # Store the question, options, correct option, tags (categories), difficulty, hint, and explanation in the document
            doc_ref.set({
                'question': question,
                'options': options,
                'correct_option': correct_option,
                'tags': tags,  # Updated field for tags (categories)
                'difficulty': difficulty,
                'hint': hint,
                'explanation': explanation,
                'category': category  # New field for category
            })

            # Add the tags (categories) to the 'categories' collection
            add_categories_to_collection(category)

            # Return a response
            return 'Question stored successfully in Firestore'
        else:
            return 'Method not allowed', 405
    except Exception as e:
        return jsonify({'error': str(e)}), 500


