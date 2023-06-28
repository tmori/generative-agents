#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

class DataModel:
    def __init__(self, name: str, contents):
        self._name = name
        self._contents = contents
        self._concrete_model = None
    
    def set_concrete_model(self, concrete_model):
        self._concrete_model = concrete_model

    def merge(self, old_model):
        self._concrete_model.merge(old_model)
        self._contents = self._concrete_model.get_contents()

    def get_name(self) -> str:
        return self._name

    def get_contents(self):
        return self._contents

    def set_content(self, content):
        self._contents = content

    def get_json_data(self):
        return {
            "name": self._name,
            "contents": self._contents
        }

    @staticmethod
    def load_json_file(filepath: str):
        if os.path.exists(filepath):
            #print("filepath=", filepath)
            with open(filepath, "r") as file:
                data = json.load(file)
                model = DataModel(data.get("name"), None)
                model._contents = data.get("contents")
                return model
        else:
            return None
