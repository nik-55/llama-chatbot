import os
from flask import Flask
from dotenv import load_dotenv

from app.controllers.session import session_blueprint
from app.controllers.pdf import pdf_blueprint
from app.controllers.chat import chat_blueprint

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.register_blueprint(session_blueprint)
    app.register_blueprint(pdf_blueprint)
    app.register_blueprint(chat_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
