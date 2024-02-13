
class _PrepromptFormat:
    def __init__(self, **kwargs) -> None:
        self.format_specs = kwargs

class _Preprompt:
    def __init__(self, value: str='') -> None:
        self.value = value

    def format(self, format: _PrepromptFormat):
        self.value = self.value.format(**format.format_specs)

    def __add__(self, other: _Preprompt):
        return _Preprompt(self.value + other.value)       

class _UserInput:
    def __init__(self, message) -> None:
        self.message = message

def pre_prompt(value: str):
    return _Preprompt(value)

def pre_prompt_format(**kwargs):
    return _PrepromptFormat(**kwargs)

def user_input(message: str):
    return _UserInput(message)