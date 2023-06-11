#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import json

class Plan:
    def __init__(self):
        self.columns = ["PlanID", "DocumentId", "Purpose", "Perspectives", "ResultID", "Status"]
        self.data = pd.DataFrame(columns=self.columns)
        self.current_id = 1

    def add_data(self, document_id, purpose, perspectives):
        data = [[self.current_id, document_id, purpose, perspectives, "", "None"]]
        new_data = pd.DataFrame(data, columns=self.columns)
        self.data = pd.concat([self.data, new_data], ignore_index=True)
        self.current_id += 1

    def update_status_doing(self, plan_id: int):
        self.data.loc[self.data["PlanID"] == plan_id, "Status"] = "Doing"

    def update_status_done(self, plan_id: int, memory_id: int):
        self.data.loc[self.data["PlanID"] == plan_id, "Status"] = "Done"
        self.data.loc[self.data["PlanID"] == plan_id, "ResultID"] = memory_id

    def save_to_json(self, file_path):
        json_data = self.data.to_dict(orient="records")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    def load_from_json(self, file_path):
        self.data = pd.read_json(file_path)

    def get_data(self):
        return self.data

    def get_data_by_id(self, plan_id=None):
        if plan_id is None:
            plan_id = self.current_id - 1
        return self.data.loc[self.data["PlanID"] == plan_id]


if __name__ == "__main__":
    plan = Plan()
    i = 0
    count = 2
    while i < count:
        doc_id = input("DocumentID> ")
        purpose = input("Purpose> ")
        perspectives = input("Perspectives> ")
        ids = input("ResultID> ")
        status = input("Status> ")
        plan.add_data(doc_id, purpose, perspectives, ids, status)
        print(plan.get_data_by_id())
        i += 1
    plan.save_to_json("test/plan.json")
