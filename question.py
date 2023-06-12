#!/usr/bin/python
# -*- coding: utf-8 -*-

from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
#from getpass import getpass
import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
tools = []

# OpenAI APIでモデルを指定して応答を取得する
def get_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": question }
        ]
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    import sys
    arg = input("> ")
    if arg == "q" or arg == "quit":
        print("See you again!")
        sys.exit(0)
    ret = get_response(arg)
    print(ret)