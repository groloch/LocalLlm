# LocalLlm #

This python repository is meant to simplify the setup of AI assistants.\
It currently contains the following features:
* local chat: a drop-in solution to self-host (or host in an environment like Colaboratory) a chat assistant ressembling ChatGPT.
* api host: a drop-in solution to host on en environment like Colaboratory a LLM-based API (like the opneAI API).
This repository is in an early phase of development and is still lacking some documentation, so feel free to open an issue if something is not working! 

## Installation ## 

Before using this repository, make sure you have `llama-cpp-python` installed and built in your environment !\
To install `llama-cpp-python`, refer to [the official guide](https://github.com/abetlen/llama-cpp-python). \
To install this repository, you can simply clone it:\
`git clone https://github.com/groloch/LocalLlm.git`

## How to use ##

On a general note, before creating your own application using this repository, you should take a look at [exmaples](examples/), this folder contains tutorials and drop-in solutions how to setup different projects !\

This project is currently based on `llama-cpp-python` and the only supported file format for models is the GGUF format.\
You can find plenty of GGUF models [here](https://huggingface.co/TheBloke)


### Local chat ###

The [local chat](examples/local_chat/) feature allows you to host a chat assistant easily !\
Read the documentation in the examples and you should be ready to go !\
The examples contain tutorials and a drop-in solution!

### API host """

The [api host](examples/api_host/) feature allows you to host a LLM-power API on web-based services like [Colaboratory](https://colab.research.google.com/). \
Read the documentation in the examples and you should be ready to go !\
The examples contain tutorials and a drop-in solution!

## . ##
