#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

from data_model import DataModel

class DocumentDataModel:
    def __init__(self, title: str):
        self.title = title
        self.results = []

    def get_title(self):
        return self.title
    
    def is_empty(self):
        if len(self.results) == 0:
            return True
        else:
            return False

    def merge(self, old_model: DataModel):
        old_contents = old_model.get_contents()
        if old_contents is None:
            return
    
        exist_contents = []
        for old_data in old_contents:
            if all(old_data.get("Answer") != entry.get("Answer") for entry in self.results):
                exist_contents.append(old_data)

        self.results += exist_contents

    def add_info(self, purpose: str, perspectives: str, answer: str, point: float):
        if not isinstance(point, float) or float(point) < 60.0:
            return
        data = {
            "Purpose": purpose,
            "Perspectives": perspectives,
            "Answer": answer,
            "Point": point
        }
        self.results.append(data)           

    def get_contents(self):
        if self.is_empty():
            return None
        return self.results
    def get_conents_num(self):
        if self.is_empty():
            return 0
        return len(self.results)
    
    def is_empty_content(self):
        return self.is_empty()

    def get_model(self) -> DataModel:
        data_model = DataModel(self.get_title(), self.get_contents())
        data_model.set_concrete_model(self)
        return data_model


    @staticmethod
    def create_from_plans(name: str, plans: dict):
        model = DocumentDataModel(name)
        if plans is not None and plans.get("Plan") is not None:
            for plan in plans.get("Plan"):
                if plan.get("DocumentID") == name:
                    #print(plan)
                    model.add_info(plan.get("Purpose"), 
                                   plan.get("Perspectives"), 
                                   plan.get("ResultID").get("Reply"),
                                   plan.get("ResultID").get("Point"))
        return model

    @staticmethod
    def load_plan_json_file(name: str, filepath: str):
        with open(filepath, "r") as file:
            plan_data = json.load(file)
            model = DocumentDataModel.create_from_plans(name, plan_data)
            return model

    @staticmethod
    def create_from_entry(name: str, entry: dict):
        model = DocumentDataModel(name)
        if entry is not None:
            for result in entry:
                model.add_info( result.get("Purpose"), 
                                result.get("Perspectives"), 
                                result.get("Answer"),
                                result.get("Point"))
        return model
    
    @staticmethod
    def load_json_file(filepath: str):
        data_model = DataModel.load_json_file(filepath)
        if data_model == None:
            return None
        model = DocumentDataModel.create_from_entry(
                    data_model.get_name(), 
                    data_model.get_contents())
        return model


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: <name> <filepath>")
        sys.exit(1)
    name = sys.argv[1]
    filepath = sys.argv[2]
    print("name=", name)
    print("filepath=", filepath)
    model = DocumentDataModel.load_plan_json_file(name, filepath)

    with open("./doc.json", "w", encoding="utf-8") as f:
        json.dump(model.get_model().get_json_data(), f, indent=4, ensure_ascii=False)

