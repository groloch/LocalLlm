## Local Chat ##

Local chat is a wrapper around llama-cpp-python that allows you to self-host (or host on an environment like Colaboratory) a chat assistant. \
This allows you to experiment with promising models, such as Llama2, Mistral7b, and more! 

### Getting started ### 

To setup a local chat, make sure you have llama-cpp-python installed. Since the installation process depends on the hardware you have, I recommend following the [official guide](https://github.com/abetlen/llama-cpp-python). \
In a colaboratory notebook, you can simply copy-paste this command :\
`!CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python`

Then, you need to get the [local_chat](../local_chat/) python module in your environment:

In a Colaboratory environment:
```python
!git clone https://github.com/groloch/LocalLlm.git
!mv LocalLlm/local_chat .
!rm -r LocalLlm 
```
This will clone the entire repository, and only keep the module we want.\
On a personal environment, it is pretty much the same: 
```python
!git clone https://github.com/groloch/LocalLlm.git
!mv LocalLlm/local_chat <your_project_folder>
!rm -r LocalLlm
```
Those simple commands should work both on linux and windows (make sure you're using powershell or git bash).

### Your first application ###

This repository contains a [drop-in solution](local_chat.ipynb) that you can directly import into Colaboratory!\
This showcases the basics of the local_chat module, but here is a quick tutorial:

#### Downloading a model ####

For that, you can either download it on the hugging face website directly, or download it directly using python (you will need to install the huggingface_hub package for that):
```python
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id=<model repository>, filename=<model name>, local_dir=<download folder>)
```
Be careful with this approach, as you only need to download the model once.

#### Setting up your assistant ####

Then you can setup your chat. The wrapper around the model is the LLMChat class:
```python
from local_chat import LLMChat
llm_chat = LLMChat(<path to the model file>)
```
To send messages, pre-prompts and pre-prompts formats to the assistant, you use the `<<` opearator.\
To retrieve messages from the assistant, you can use the `>>` operator. This operator takes a function and the LLM will stream the answer to the prompt to that function. If you want the LLM to stream in the console, use `None`.\
Here is a quick example on how to setup a command-line chat assistant:
```python
from local_chat import user_input, pre_prompt, pre_prompt_format

llm_chat << pre_prompt('You are a chat assistant specialized in {topic}')

topic = input('What do you want your assistant to be specialized in ?\n')
llm_chat << pre_prompt_format(topic=topic)

for _ in range(5):
    message = input('user: ')
    llm_chat << user_input(message)

    llm_chat >> None
```
If you want to start a new chat, you need to call the `reset` function, this will clear the LLM internal memory:
```python
llm_chat.reset()
llm_chat << user_input('What are you specialized in ?')
llm_chat >> None
```
