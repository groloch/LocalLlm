from flask import Flask
from flask_cloudflared import run_with_cloudflared


class ApiHost:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        run_with_cloudflared(self.app)

        @self.app.route('/')
        def home():
            return 'Hello, this is hosted on google colab!'
        
        @self.app.route('/api')
        def api():
            return 'Api page, to be used by clients only !'

    def run(self):
        self.app.run()

if __name__ == '__main__':
    host = ApiHost()
    host.run()