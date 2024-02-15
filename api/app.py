from flask import Flask
from flask_socketio import SocketIO, namespace
from flask_cloudflared import run_with_cloudflared

class ApiNamespace(namespace.Namespace):
    def __init__(self, namespace: str, sio: SocketIO) -> None:
        super().__init__(namespace)
        self.sio = sio

    def on_connect(self):
        print('Hello to our new user !')

class ApiHost:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.sio = SocketIO(self.app)
        run_with_cloudflared(self.app)

        @self.app.route('/')
        def home():
            return 'Hello, this is hosted on google colab!'

    def run(self):
        self.app.run()