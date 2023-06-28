#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from data_model import DataModel
from data_model_storage import DataModelStorage

class DataModelAccessor:
    def __init__(self, dir: str):
        self.directory = dir
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.datamodel_path = os.path.join(self.directory, "data_model")
        self.data_model_storage = DataModelStorage(self.datamodel_path)
        self._load_file_cache()

    def _load_file_cache(self):
        self.file_cache = []
        for file_name in os.listdir(self.datamodel_path):
            if file_name.endswith(".json"):
                name = file_name[:-5]  # .json 拡張子を除去
                self.file_cache.append(name)

    def add_data_model(self, name: str, contents: str):
        data_model = DataModel(name, contents)
        self.data_model_storage.save_data_model(data_model)

        if name not in self.file_cache:
            self.file_cache.append(name)

    def add_data_model(self, model: DataModel):
        self.data_model_storage.save_data_model(model)

        if model.get_name() not in self.file_cache:
            self.file_cache.append(model.get_name())


    def get_data_model(self, name: str) -> DataModel:
        if name in self.file_cache:
            return self.data_model_storage.load_data_model(name)
        else:
            return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <dir>")
        sys.exit(1)
    dir = sys.argv[1]
    accessor = DataModelAccessor(dir)
    #accessor.add_data_model("term1", "info1")
    #accessor.add_data_model("term1", "info2")
    #accessor.add_data_model("term2", "info1")

    model = accessor.get_data_model("term3")
    if model is not None:
        print(model.get_json_data())
    else:
        print("Not Found")
