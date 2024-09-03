from flask import Flask, request, jsonify
from flask_cors import cross_origin
from notion_AI_agent import query, SendToNotion
app = Flask(__name__)


@app.route("/post_query", methods=["POST"])
def post_query():
    # Get the JSON data from the request
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Pass the question to the query function
    result = query(question)

    return jsonify(result)


@app.route('/send-to-notion', methods=['POST'])
@cross_origin()
def send_to_notion():
    try:
        data = request.json
        notionAPIkey = data.get('api_key')
        parentPageIds = data.get('parent_page_ids')  # Assuming parent page IDs are passed here
        question = data.get('question')
        size = len(parentPageIds)

        # Simulating OpenAI response for the question
        openai_response = query(question, size)
        openai_response = openai_response.get('response')

        app.logger.info(openai_response)

        # Call the function to send the response to Notion
        result = SendToNotion(openai_response, notionAPIkey, parentPageIds)
        return jsonify(result)

    except Exception as e:
        # Log the error to the console
        print(f"Error occurred: {str(e)}")
        # Return a response with the error message
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
