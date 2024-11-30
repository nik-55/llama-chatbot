import os
from flask import Blueprint, session, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.services.rag import add_documents_to_vector_store, get_documents
from app.db import db

pdf_blueprint = Blueprint('routes', __name__)

@pdf_blueprint.route('/pdf/upload/', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        dir_path = os.path.join(current_app.config['UPLOAD_FOLDER'], session['key'])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        filename = secure_filename(file.filename)
        file_path = os.path.join(dir_path, filename)
        file.save(file_path)
        db[session['key']]['pdf_paths'].append(file_path)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    
    return jsonify({'error': 'Invalid file format. Please upload a PDF.'}), 400

@pdf_blueprint.route('/pdf/process/', methods=['GET'])
def process_pdf():
    vector_store = db[session['key']]['vector_store']
    file_path = db[session['key']]['pdf_paths'][0]
    docs = get_documents(file_path)
    add_documents_to_vector_store(vector_store, docs)
    return jsonify({'message': 'PDF processed successfully'}), 200

