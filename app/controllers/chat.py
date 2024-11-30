from flask import Blueprint, request, session, jsonify

from app.services.rag import get_answer
from app.db import db

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/question/', methods=['POST'])
def ask_question():
    vector_store = db[session['key']]['vector_store']
    question = request.json['question']
    response = get_answer(vector_store, question)
    db[session['key']]['mssgs'].append({
        'question': question,
        'response': response
    })
    return jsonify({'response': response}), 200

@chat_blueprint.route('/messages/', methods=['GET'])
def get_messages():
    mssgs = db[session['key']]['mssgs']
    return jsonify({'messages': mssgs}), 200
