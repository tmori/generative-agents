#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

class MemoryStream:
    def __init__(self):
        self.data = pd.DataFrame(columns=["ID", "TargetDocID", "Question", "Reply"])
        self.current_id = 1

    def add_data(self, target_doc_id, question, reply):
        data = [[self.current_id, target_doc_id, question, reply]]
        new_data = pd.DataFrame(data, columns=["ID", "TargetDocID", "Question", "Reply"])
        self.data = pd.concat([self.data, new_data], ignore_index=True)
        self.current_id += 1

    def get_data(self):
        return self.data

if __name__ == "__main__":
    memory_stream = MemoryStream()
    while True:
        target_doc_id = input("TargetDocID> ")
        question = input("question> ")
        reply = input("reply> ")
        memory_stream.add_data(target_doc_id, question, reply)
        print(memory_stream.get_data())
else:
    pass
