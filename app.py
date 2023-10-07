from flask import Flask, render_template, request, jsonify

import json
import spacy

# Load the JSON data
with open('DataSet/Dataset.json', 'r') as file:
    data = json.load(file)

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")





app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


def get_Chat_response(text):

    max_similarity = 0
    best_answer = None

    for qna in data['questions']:
        question = qna['question']
        similarity = nlp(question).similarity(nlp(text))
        if similarity > max_similarity:
            max_similarity = similarity
            best_answer = qna['answer']

    if max_similarity < 0.5:
        return "This detail is yet to be discovered."
    return best_answer


if __name__ == '__main__':
    app.run()
