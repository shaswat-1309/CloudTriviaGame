from google.cloud import firestore
from google.cloud import language_v1
from flask import jsonify, make_response

db = firestore.Client()
language_client = language_v1.LanguageServiceClient()


def editquestion(request):
    try:

        if request.method == 'OPTIONS':
            # Handle preflight request for CORS
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST')
            return response

        if request.method == 'POST':
            # Retrieve the question ID and updated question data from the request JSON payload
            request_json = request.get_json()
            document_id = request_json['id']

            # Retrieve the existing question data from Firestore
            doc_ref = db.collection('questions').document(document_id)
            existing_question_data = doc_ref.get().to_dict()

            # Create a copy of the request data and remove the ID field
            updated_question_data = request_json.copy()
            updated_question_data.pop('id', None)

            # Check if the category has changed
            if 'category' in updated_question_data and existing_question_data.get('category') != updated_question_data['category']:
                # Call the add_to_categories function to update categories
                add_categories_to_collection(updated_question_data['category']) # Replace 'add_to_categories' with the actual function name

            # Update only the changed fields in the existing_question_data dictionary
            for field, value in updated_question_data.items():
                if field in existing_question_data and existing_question_data[field] != value:
                    existing_question_data[field] = value

            # Check if either the question or the hint has changed
            if 'question' in updated_question_data or 'hint' in updated_question_data:
                # Concatenate the updated question and hint
                updated_question = existing_question_data.get('question', '')
                updated_hint = existing_question_data.get('hint', '')
                combined_text = f"{updated_question} {updated_hint}".strip()

                # Determine the category of the question using Natural Language API
                tags = determine_tags(combined_text)
                existing_question_data['tags'] = tags

            # Update the question data in the Firestore document
            doc_ref.update(existing_question_data)

            response_data = jsonify(existing_question_data)

            # Add CORS headers to the response
            response = make_response(response_data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST')

            return response

        else:
            return ('Method not allowed', 405)

    except Exception as e:
        return (f'Error occurred: {e}', 500)

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

def add_categories_to_collection(category):
    # Add the category to the 'categories' collection
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
