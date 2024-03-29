from llama_cpp import Llama
from huggingface_hub import hf_hub_download


class _ModelWrapper:
    def __init__(self, repo_id: str, file_name: str) -> None:
        self.repo_id = repo_id
        self.file_name = file_name
        self.llm = None

    def download_model(self):
        if self.repo_id is None or self.file_name is None:
            #Error model not downloable
            pass
        self.model_path = hf_hub_download(repo_id=self.repo_id, filename=self.file_name)

    def load_model(self):
        pass

    def __eq__(self, model_path: tuple):
        return len(model_path) == 2 and \
               self.repo_id == model_path[0] and \
               self.file_name == model_path[1]


class ModelInput:
    def __init__(self, inputs: str | list) -> None:
        if isinstance(inputs, str):
            self.type = 'completion'
            self.content = inputs
        if isinstance(inputs, list):
            self.type = 'chat'
            self.content = inputs


class Query:
    def __init__(self, query_dict: dict) -> None:
        self.errors = []
        self.valid_tasks = ('text_generation', 'none')
        self.parameters = {
            'top_k': 10,
            'top_p': 0.95,
            'temperature': 1,
            'max_token': 512
        }
        self.options = {
            'use_gpu': True,
            'ctx_length': 4096,
            'chat_format': 'llama-2'
        }

        if 'task' in query_dict:
            self.task = query_dict['task']
            if self.task not in self.valid_tasks:
                self.errors.append(f'Invalid task {self.task}, valid tasks are: ', 
                                   *self.valid_tasks)
        else:
            self.errors.append('`task` field must be specified\n')

        if 'repo_id' in query_dict:
            self.repo_id = query_dict['repo_id']
        else:
            self.errors.append('`repo_id` field must be specified\n')

        if 'file_name' in query_dict:
            self.file_name = query_dict['file_name']
        else:
            self.errors.append('`file_name` field must be specified\n')

        self.model = (self.repo_id, self.file_name)

        if 'inputs' in query_dict:
            self.model_inputs = ModelInput(query_dict['inputs'])
        
        if 'parameters' in query_dict:
            self.update_parameters(query_dict['parameters'])
        
        if 'options' in query_dict:
            self.update_options(query_dict['options'])
    
    def update_parameters(self, parameters):
        if 'max_tokens' in parameters:
            self.parameters['max_tokens'] = parameters['max_tokens']
        if 'top_k' in parameters:
            self.parameters['top_k'] = parameters['top_k']
        if 'top_p' in parameters:
            self.parameters['top_p'] = parameters['top_p']
        if 'temperature' in parameters:
            self.parameters['temperature'] = parameters['temperature']

    def update_options(self, options):
        if 'use_gpu' in options:
            self.options['use_gpu'] = options['use_gpu']
        if 'ctx_length' in options:
            self.options['ctx_length'] = options['ctx_length']
        if 'chat_format' in options:
            self.options['chat_format'] = options['chat_format']


class TextGenerationModel(_ModelWrapper):
    def __init__(self, repo_id: str = None, file_name: str = None) -> None:
        super().__init__(repo_id, file_name)

    def generate_answer(self, query: Query):
        genargs = query.parameters
        top_k = genargs['top_k']
        top_p = genargs['top_p']
        temperature = genargs['temperature']
        max_tokens = genargs['max_tokens']
        inputs = query.model_inputs

        if inputs.type == 'completion':
            outputs = self.llm(inputs.content,
                               max_tokens=max_tokens,
                               mop_k=top_k,
                               mop_p=top_p,
                               memperature=temperature,
                               mcho = False)
            outputs = outputs['choices'][0]['text']
        elif inputs.type == 'chat':
            outputs = self.llm.create_chat_completion(inputs.content,
                                                      max_tokens=max_tokens,
                                                      top_k=top_k,
                                                      top_p=top_p,
                                                      temperature=temperature)
            outputs = outputs['choices'][0]['message']
        return outputs

    def load_model(self, query: Query):
        options = query.options
        if options['use_gpu']:
            n_gpu_layers = -1
        else:
            n_gpu_layers = 0
        ctx_length = options['ctx_length']
        chat_format = options['chat_format']

        self.llm = Llama(self.model_path,
                           n_gpu_layers=n_gpu_layers,
                           n_ctx=ctx_length,
                           chat_format=chat_format)
        

def create_model(query: Query):
    match query.task:
        case 'text_generation':
            model = TextGenerationModel(query.repo_id,
                                        query.file_name)
        case _:
            return None
            
    model.download_model()
    model.load_model(query)
    return model
