import string
import random

from flask import Flask
from flask import request, jsonify
from flask_cloudflared import run_with_cloudflared

from . import Query, create_model


class ApiHost:
    def __init__(self, use_token=True) -> None:
        self.app = Flask(__name__)
        run_with_cloudflared(self.app)
        self.use_token = use_token
        self.access_token = None
        if self.use_token:
            self.generate_access_token()
        self.model = None

        @self.app.route('/')
        def home():
            return 'Hello, this is hosted on google colab!'
        
        @self.app.route('/api', methods=['POST'])
        def api():
            received_data = request.json

            if self.use_token:
                if received_data['token'] != self.access_token:
                    return jsonify({'error': 'wrong token'}), 403
                
            query = Query(received_data)
            if len(query.errors != 0):
                return jsonify(query.errors), 400
            
            if self.model != query.model:
                self.model = create_model(query)

            answer = self.model.generate_answer(query)

            return jsonify({'answer': answer}), 200
        
    def run(self):
        self.app.run()

    def generate_access_token(self):
        chars = string.ascii_letters + string.digits

        self.access_token = ''.join(random.choices(chars, k=20))

        print('Access token for the current session:', self.access_token)
    

if __name__ == '__main__':
    host = ApiHost()
    host.run()