#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import traceback
from data_model_accessor import DataModelAccessor
from reflection_data_model import ReflectionDataModel

class ReflectionDataPersistentor:
    def __init__(self, accessor: DataModelAccessor):
        self.accessor = accessor

    def save_reflection_data(self):
        for model in self.models:
            data_model = model.get_model()
            data_model.set_concrete_model(model)
            self.accessor.add_data_model(data_model)

    def load_reflection_data(self, reflection_data_path: str):
        try:
            with open(reflection_data_path, "r") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            traceback_str = traceback.format_exc()
            error_message = f"ERROR: {str(e)}"
            print(traceback_str + error_message)
            return
        
        self.models = []
        for entry in json_data.get("Knowledges"):
            #print("Term:", entry.get("Term"))
            model = ReflectionDataModel(entry.get("Term").replace(" ", "_"))
            if entry.get("KnownInfos") is not None:
                for known_info in entry.get("KnownInfos"):
                    #print("KnownInfo:", known_info.get("KnownInfo"))
                    #print("DocumentIDs:", known_info.get("DocumentIDs"))
                    model.add_info(known_info.get("KnownInfo"), known_info.get("DocumentIDs"))
            if entry.get("Relations") is not None:
                model.add_relations(entry.get("Relations"))
            if entry.get("UnknownInfo") is not None:
                model.update_unknown_info(entry.get("UnknownInfo"))
            self.models.append(model)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: <dir> <filepath>")
        sys.exit(1)
    dir = sys.argv[1]
    filepath = sys.argv[2]
    accessor = DataModelAccessor(dir)

    persistentor = ReflectionDataPersistentor(accessor)
    persistentor.load_reflection_data(filepath)
    persistentor.save_reflection_data()
    