from flask import Blueprint, session, jsonify, render_template

from app.services.rag import create_vector_store
from app.db import db

session_blueprint = Blueprint('home', __name__)

@session_blueprint.route('/')
def home():
    return render_template('index.html')

@session_blueprint.route('/sessions/', methods=['GET'])
def get_session_key():
    import uuid
    session_key = str(uuid.uuid4())
    session['key'] = session_key

    db[session_key] = {
        'vector_store': create_vector_store(),
        'pdf_paths': [],
        'mssgs': []
    }
    return jsonify({'message': 'Session key set successfully'}), 200
