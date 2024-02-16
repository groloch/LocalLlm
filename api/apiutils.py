from llama_cpp import Llama
from huggingface_hub import hf_hub_download


class _ModelWrapper:
    def __init__(self, repo_id: str, file_name: str) -> None:
        self.repo_id = None
        self.file_name = None
        self.llm = None

    def download_model(self):
        if self.repo_id is None or self.file_name is None:
            #Error model not downloable
            pass
        self.model_path = hf_hub_download(repo_id=self.repo_id, filename=self.file_name)

    def load_model(self):
        pass

class ModelInput:
    def __init__(self, inputs: str | dict) -> None:
        if isinstance(inputs, str):
            self.type = 'completion'
            self.content = inputs
        if isinstance(inputs, dict):
            self.type = 'chat'
            self.content = inputs
    
    def __eq__(self, model_path: tuple):
        return len(model_path) == 2 and \
               self.repo_id == model_path[0] and \
               self.file_name == model_path[1]


class Query:
    def __init__(self, query_dict: dict) -> None:
        self.errors = []
        self.valid_tasks = ('text_generation', 'none')

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
        
        if 'generation_kwargs' in query_dict:
            self.generation_kwargs = query_dict['generation_kwargs']
        else:
            self.generation_kwargs = {
                'do_sample': False,
                'max_tokens': 512,
                'temperature': 1
            }
        
        if 'model_kwargs' in query_dict:
            self.model_kwargs = query_dict['model_kwargs']
        else:
            self.model_kwargs = {
                'use_gpu': True,
                'ctx_length': 4096
            }


class TextGenerationModel(_ModelWrapper):
    def __init__(self, repo_id: str = None, file_name: str = None) -> None:
        super.__init__(repo_id, file_name)

    def generate_answer(self, query: Query):
        genargs = query.generation_kwargs
        if not genargs['do_sample']:
            top_k = 1
        else:
            top_k = genargs['top_k']
        top_p = genargs['top_p']
        temperature = genargs['temperature']
        max_tokens = genargs['max_tokens']
        inputs = query.model_inputs

        if inputs.type == 'completion':
            outputs = self.llm(inputs.content,
                                 max_tokens=max_tokens,
                                 top_k=top_k,
                                 top_p=top_p,
                                 temperature=temperature,
                                 echo = False)
        elif inputs.type == 'chat':
            outputs = self.llm.create_chat_completion(inputs.content,
                                                        max_tokens=max_tokens,
                                                        top_k=top_k,
                                                        top_p=top_p,
                                                        temperature=temperature,
                                                        echo=False)
        outputs = outputs['choices'][0]['text']
        return outputs

    def load_model(self, query: Query):
        if query['model_kwargs']['use_gpu']:
            n_gpu_layers = -1
        else:
            n_gpu_layers = 0
        ctx_length = query['model_kwargs']['ctx_length']
        chat_format = query['model_kwargs']['chat_format']

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
    model.load_model()
    return model
