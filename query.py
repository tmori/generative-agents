#!/usr/bin/python
# -*- coding: utf-8 -*-
from document_db import load_db_with_type
from prompt_template import PromptTemplate
from memory_stream import MemoryStream

class Query:
    def __init__(self, target_doc_id: str, main_question: str, memory_stream: MemoryStream, db_dir: str):
        self.target_doc_id = target_doc_id
        self.main_question = main_question
        self.memory_stream = memory_stream
        self.qa = load_db_with_type(db_dir)

    def run(self, prompt_template_path: str, sub_question: str):
        prompt_query_template = PromptTemplate(prompt_template_path)
        # Generate the prompt query using the template and inputs
        query = prompt_query_template.get_prompt(sub_question=sub_question)
        reply = self.qa({"question": query})

        #calculate point of reply
        point = 10

        # Store the information in the MemoryStream
        self.save(sub_question, reply["answer"], point)

    def save(self, sub_question: str, reply: str, point: int):
        # Store the information in the MemoryStream
        self.memory_stream.add_data(
            target_doc_id = self.target_doc_id, 
            question = sub_question, 
            reply = reply, 
            point = point)


if __name__ == "__main__":
    import sys
    db_dir = "../DB"
    memory_stream = MemoryStream()
    prompt_template_path = "./ptemplate_query.txt"
    query = Query("1", "Athrillとは何ですか？", memory_stream, db_dir)
    while True:
        question = input("question> ")
        if question == 'exit' or question == 'q' or question == "quit":
            print("See you again!")
            sys.exit(0)
        query.run(prompt_template_path, question)
        print(memory_stream.get_reply())
else:
    pass