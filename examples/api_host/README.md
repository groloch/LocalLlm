## API Host ##

API host is a module allowing to host a LLM-powered API on online computing resources, like Colaboratory or Kaggle.\
This allows you to experiment with promising models, such as Llama2, Mistral7b, and more! \
This example folder contains a drop-in solution for a host (on Colaboratory) and for a client (on your own computer) !


### Getting started ### 

To setup an API Host, make sure you have llama-cpp-python and flask-cloudflared installed.\
In a colaboratory notebook, you can simply copy-paste this command :\
```python
!CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
!pip install flask-cloudflared
```

Then, you need to get the [api_host](../api_host/) python module in your environment:

In a Colaboratory environment:
```python
!git clone https://github.com/groloch/LocalLlm.git
!mv LocalLlm/api_host .
!rm -r LocalLlm 
```
This will clone the entire repository, and only keep the module we want.\

### Your first application ###

This repository contains a [drop-in solution](api_host.ipynb) that you can directly import into Colaboratory!\
This showcases the basics of the api_host module, but here is a quick tutorial:

#### Setting up your API ####

To setup an APi Host is a fairly easy task, all you need to do is to import the `ApiHost` class and instantiate it:
```python
from api import ApiHost
host = ApiHost()
host.run()
```
This is the way to setup an API with a generated access token, that you will have to pass into your requests to the API. This is the recommended way to setup an API for security reasons. For convenience, you can also setup the API without access token:
```python
from api import ApiHost
host = ApiHost(use_token=False)
host.run()
```
And that's it ! Your API should be running now!

#### Send requests #### 

Now that your api is running, you can start to send some requests. First of all you need to get the generated access token (if you're using one) and url for the session (these change everytime you restart the API).\
The access token is in the first line printed when the API is starting.\
There are 2 urls printed when the API is starting. The one you should copy is the one ending with `trycloudflared.com`. I recommend visiting the url from you browser at least once since the url may not work. In this cas, rerun the cell and a new url should be generated.

You can finally setup your client ! The client is a python program that will run on your computer, that will send requests (prompts) to the LLM hosted by the API. For that you need the requests package:
```python
pip install requests
```
You can then send requests to the API. The requests take 
```python
import requests

payload = {
    'token': <You access token>,
    'task': 'text_generation',
    'repo_id': <repo id for the model>,
    'file_name': <file name for the model>,
    'inputs': 'Hello ! Today I can do these activities:',
    'parameters': {},
    'options': {}
}
anwser = requests.post(f'{<your url>}/api'}, json=payload)
``` 
The `repo_id` and the `file_name` fields contain the hugging face repo id and file name for the model you want to host.

The `inputs` can be of 2 different types: either a string, in which case the answer will be a text completion of this string, or a list containing a chat history, in which case the answer will be the assistant anwser to the chat history. Here is an example of chat history:
```python
'inputs': [
    {'role': 'system', 'content': 'You are an assistant specialized in story writing'},
    {'role': 'user', 'content': 'Write a story about a cat stealing food from its owner.'}
]
```
You should distribute the roles this way:
* `'system'` is optional and should be the first message in the chat history
* `'user'` and `'assistant'` should be following one another, `'user'` containing the user messages and `'assistant'` containing the LLM response.

The `options` field is a dictionnary that can contain 3 fields:
* `use_gpu`: if your host environment has a GPU or not (default: True)
* `ctx_lenght`: context length of the hosted model (default: 4096)
* `chat_format`: the chat format used to generate the special tokens if the input is in chat mode.

The `parameters` field is a dictionnary that can contain the following fields:
* `max_tokens`: the maximum number of tokens generated
* `top_k`: the top_k parameter for tokens sampling  (set to 1 for no sampling)
* `top_p`: the top_p parameter for tokens sampling.
* `temperature`: the temperature parameter for tokens sampling.

#### Retrieve answers #### 

Once your request has been sent to the API, it may take some time to process, depending on the model you're running, if it's the first request on this model (the host will need to download it), the `max_tokens` parameter you specified, etc.\
When the request has been processed, you get a `anwser` object. To retrieve the dictionnary containing the generated text, you need to call the `json` function:
```python
generated_text = answer.json()['answer']['content']
```
You can then do whatever you want with this generated text ! 