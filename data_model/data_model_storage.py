#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json

from data_model import DataModel

class DataModelStorage:
    def __init__(self, directory: str):
        self.directory = directory
        
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_data_model(self, data_model: DataModel, merge: bool  = True):
        filename = f"{data_model.get_name()}.json"
        filepath = os.path.join(self.directory, filename)

        model = DataModel.load_json_file(filepath)
        if merge and model is not None:
            model.add_content(data_model.get_contents())
        else:
            model = data_model

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(model.get_json_data(), f, indent=4, ensure_ascii=False)
    
    def load_data_model(self, name: str) -> DataModel:
        filename = f"{name}.json"
        filepath = os.path.join(self.directory, filename)
        return DataModel.load_json_file(filepath)
    

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: <dir> <name> <contents>")
        sys.exit(1)
    dir = sys.argv[1]
    storage = DataModelStorage(dir)
    model = DataModel(sys.argv[2], sys.argv[3])
    storage.save_data_model(model)
    