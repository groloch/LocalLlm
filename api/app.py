import string
import random
from IPython.display import HTML, display

from flask import Flask
from flask import request, jsonify
from flask_cloudflared import run_with_cloudflared


class ApiHost:
    def __init__(self, notebook=False) -> None:
        self.app = Flask(__name__)
        run_with_cloudflared(self.app)
        self.notebook = notebook

        @self.app.route('/')
        def home():
            return 'Hello, this is hosted on google colab!'
        
        @self.app.route('/api', methods=['POST'])
        def api():
            received_data = request.json
            print('Data received!', received_data, sep='\n')
            if self.notebook:
                if received_data['token'] != self.access_token:
                    return jsonify({'error': 'wrong token'}), 403
            return jsonify({}), 200
        
        self.access_token = None

    def run(self):
        self.app.run()

    def generate_access_token(self):
        chars = string.ascii_letters + string.digits

        self.access_token = ''.join(random.choices(chars, k=20))

        html_code = f''
        f'<input type="text" value="{self.access_token}"> id="access_token" '
        f'readonly style="border: none; background-color: white;>'
        f'<button onclick="navigator.clipboard.writeText(document.getElementById("access_token").value)">'
        f'  Copy to clipboard'
        f'</button>'

        display(HTML(html_code))
        


if __name__ == '__main__':
    host = ApiHost()
    host.run()