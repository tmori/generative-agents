#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

class DataModel:
    def __init__(self, name: str, contents: str):
        self._name = name
        if contents is not None:
            if not isinstance(contents, str):
                raise ValueError("contents must be a string")
            self._contents = [contents]
        else:
            self._contents = []
    
    def get_name(self) -> str:
        return self._name

    def get_contents(self) -> list:
        return self._contents

    def add_content(self, content: list):
        self._contents += content

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
