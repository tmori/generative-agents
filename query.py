#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from prompt_template import PromptTemplate
from memory_stream import MemoryStream

class Query:
    def __init__(self, target_doc_id: str, main_question: str, memory_stream: MemoryStream, qa):
        self.target_doc_id = target_doc_id
        self.main_question = main_question
        self.memory_stream = memory_stream
        self.qa = qa

    def run(self, prompt_template_path: str, sub_question: str):
        prompt_query_template = PromptTemplate(prompt_template_path)
        # Generate the prompt query using the template and inputs
        query = prompt_query_template.get_prompt(sub_question=sub_question)
        reply = self.qa({"question": query})

        #calculate point of reply
        match = re.search(r"Point: ?([0-9\.]+)$", reply["answer"])
        if match:
            point = float(match.group(1))
            # Store the information in the MemoryStream
            return self._save(sub_question, reply["answer"], point)
        else:
            print("ERROR: can not find point in reply:" + reply["answer"])
            return -1

    def _save(self, sub_question: str, reply: str, point: int):
        # Store the information in the MemoryStream
        return self.memory_stream.add_data(
            target_doc_id = self.target_doc_id, 
            question = sub_question, 
            reply = reply, 
            point = point)


if __name__ == "__main__":
    import sys
    from db_manager import get_qa
    db_dir = ".."
    doc_id = "DB"
    qa = get_qa(db_dir, doc_id)
    memory_stream = MemoryStream()
    prompt_template_path = "./prompt_templates/ptemplate_query.txt"
    query = Query("1", "Athrillとは何ですか？", memory_stream, qa)
    while True:
        question = input("question> ")
        if question == 'exit' or question == 'q' or question == "quit":
            print("See you again!")
            sys.exit(0)
        query.run(prompt_template_path, question)
        print("REPLY: " + memory_stream.get_reply())
        print("POINT: " + str(memory_stream.get_point()))
else:
    pass