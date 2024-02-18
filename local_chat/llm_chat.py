from llama_cpp import Llama

from .chatutils import _Preprompt, _PrepromptFormat, _UserInput


class _ChatHistory:
    def __init__(self) -> None:
        self.system_message = _Preprompt()
        self.chat_messages = []

    def add_preprompt(self, pp: _Preprompt):
        self.system_message += pp

    def format_preprompt(self, format: _PrepromptFormat):
        self.system_message.format(format)

    def add_chat_message(self, message: dict):
        if len(self.chat_messages) > 0 and self.chat_messages[-1]['role'] == message['role']:
            self.chat_messages[-1]['content'] += message['content']
        else:
            self.chat_messages.append(message)
        
    def get_llm_input(self):
        llm_input = [
            {'role': 'system',
             'content': self.system_message.value}
        ]
        [llm_input.append(message) for message in self.chat_messages]
        return llm_input


class LLMChat:
    def __init__(self, model_path, chat_format='llama-2', 
                 n_gpu_layers=-1, n_ctx=4096) -> None:
        self.llm = Llama(model_path=model_path, 
                         chat_format=chat_format, 
                         n_gpu_layers=n_gpu_layers,
                         n_ctx=n_ctx)
        self.chat_history = _ChatHistory()

    def stream_answer(self, print_fn):
        streamer = self.llm.create_chat_completion(self.chat_history.get_llm_input(),
                                                   stream=True)
        generated_text = ''
        for chunk in streamer:
            delta = chunk['choices'][0]['delta']
            if 'role' in delta:
                print_fn(delta['role'], end=': ')
            elif 'content' in delta:
                print_fn(delta['content'], end='')
                generated_text += delta['content']

        self.chat_history.add_chat_message({
            'role': 'assistant',
            'content': generated_text
        })

    def reset(self):
        self.chat_history = _ChatHistory()

    def __lshift__(self, other):
        if isinstance(other, _Preprompt):
            self.chat_history.add_preprompt(other)
        elif isinstance(other, _PrepromptFormat):
            self.chat_history.format_preprompt(other)
        elif isinstance(other, _UserInput):
            self.chat_history.add_chat_message({
                'role': 'user', 
                'content': other.message
            })

    def __rshift__(self, other):
        if callable(other):
            print_fn = other
        else:
            print_fn = lambda *args, **kwargs: print(*args, flush=True, **kwargs)

        self.stream_answer(print_fn)