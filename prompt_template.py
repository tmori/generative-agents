#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class PromptTemplate:
    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.template = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")

    def get_prompt(self, **kwargs) -> str:
        return self.template.format(**kwargs)

if __name__ == "__main__":
    pt = PromptTemplate("./prompt_templates/ptemplate_query.txt")
    while True:
        target_doc_id = input("TargetDocID> ")
        question = input("question> ")
        reply = input("reply> ")
        point = input("point> ")
        prompt = pt.get_prompt(TargetDocID=target_doc_id, question=question, reply=reply, point=int(point))
        print("PROMPT:\n" +prompt)
