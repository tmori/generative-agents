#!/usr/bin/python
# -*- coding: utf-8 -*-

from memory_stream import MemoryStream

class HistorySelector:
    def __init__(self, memory_stream):
        self.memory_stream = memory_stream
        self.history = []

    def select(self, threshold):
        data = self.memory_stream.get_data()
        high_point_data = data[data["Point"] >= threshold]
        self.history = high_point_data
        return high_point_data

    def get_history(self):
        return self.history


if __name__ == "__main__":
    memory_stream = MemoryStream()
    data_num = input("DataNum> ")
    count = int(data_num)
    i = 0
    while i < count:
        target_doc_id = input("TargetDocID> ")
        question = input("question> ")
        reply = input("reply> ")
        point = input("point> ")
        memory_stream.add_data(target_doc_id, question, reply, int(point))
        print(memory_stream.get_data())
        i += 1
    threshold = input("Threshold> ")
    history = HistorySelector(memory_stream)
    print(history.select(int(threshold)))
else:
    pass
