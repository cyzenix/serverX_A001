import os
import re
import difflib
import random
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EXPECTED_ORIGIN = 'https://chatzenix.github.io/cyzenix/chat1.html'
SECRET_API_KEY = '72472hSujsOitwoO,0($9#7@)juaiwoq09uYajaiuaiiqywuzkIsu~{}'

script_dir = os.path.dirname(os.path.realpath(__file__))
responses_file_path = os.path.join(script_dir, 'responses.json')

with open(responses_file_path, 'r', encoding='utf-8') as responses_file:
    responses = json.load(responses_file)

apologies = [
    "Mujhe khed hai, main iska jawab nahi de sakta.",
    "Maafi chahata hoon, main abhi seekh raha hoon aur mujhe jawab nahi pata.",
    "Sorry, mujhe is bare mein kuch nahi pata.",
]

def get_random_apology():
    return random.choice(apologies)

def chatbot_response(user_input):
    user_input = re.sub(r'\W+', '', user_input.lower())

    if user_input in responses:
        return responses[user_input]

    for key, value in responses.items():
        cleaned_key = re.sub(r'\W+', '', key.lower())
        score = difflib.SequenceMatcher(None, user_input, cleaned_key).ratio()
        if score > 0.8:
            return value

    best_response = find_best_response(user_input, responses)
    if best_response:
        return best_response

    return get_random_apology()

def find_best_response(user_input, responses):
    cleaned_user_input = re.sub(r'\W+', '', user_input.lower())

    sorted_responses = sorted(responses, key=lambda response: difflib.SequenceMatcher(None, cleaned_user_input, re.sub(r'\W+', '', response.lower())).ratio(), reverse=True)

    best_response = sorted_responses[0] if sorted_responses else None
    max_score = 0.7

    if difflib.SequenceMatcher(None, cleaned_user_input, re.sub(r'\W+', '', best_response.lower())).ratio() > max_score:
        return best_response

    return get_random_apology()

@app.route('/', methods=['POST'])
def chatbot_endpoint():
    user_input = request.json.get('text', '')
    if not user_input:
        return jsonify({"status": "error", "message": "No input provided"})

    response = chatbot_response(user_input)
    return jsonify({"status": "success", "response": response})

if __name__ == '__main__':
    app.run(debug=True)
