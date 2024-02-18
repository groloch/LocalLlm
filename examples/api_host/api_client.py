import requests

url = input('url: ')

payload={
    'task': 'text_generation',
    'repo_id': 'TheBloke/Mistral-7B-Instruct-v0.2-GGUF',
    'file_name': 'mistral-7b-instruct-v0.2.Q5_K_S.gguf',
    'inputs': [{'role': 'user', 'content': 'What activities can I do today ?'}],
    'parameters': {
        'top_k': 1,
        'max_tokens': 1024
    }
}

answer = requests.post(url=url, json=payload)

print(answer.json()['answer']['content'])