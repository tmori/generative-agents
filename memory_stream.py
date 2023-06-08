#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

class MemoryStream:
    def __init__(self):
        self.columns = ["ID", "TargetDocID", "Question", "Reply", "Point"]
        self.data = pd.DataFrame(columns=self.columns)
        self.current_id = 1

    def add_data(self, target_doc_id, question, reply, point):
        data = [[self.current_id, target_doc_id, question, reply, point]]
        new_data = pd.DataFrame(data, columns=self.columns)
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
        point = input("point> ")
        memory_stream.add_data(target_doc_id, question, reply, int(point))
        print(memory_stream.get_data())
else:
    pass
