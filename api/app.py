from flask import Flask
from flask import request
from flask_cloudflared import run_with_cloudflared


class ApiHost:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        run_with_cloudflared(self.app)

        @self.app.route('/')
        def home():
            return 'Hello, this is hosted on google colab!'
        
        @self.app.route('/api', methods=['POST'])
        def api():
            print('Post request received !')
            print('JSON', request.json)
            print('FORM', request.form)

    def run(self):
        self.app.run()

if __name__ == '__main__':
    host = ApiHost()
    host.run()