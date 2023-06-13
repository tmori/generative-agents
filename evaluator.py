#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import json
from memory_stream import MemoryStream
from plan import Plan
from prompt_template import PromptTemplate
from question import get_response
from plan import Plan
import copy

class Evaluator:
    def __init__(self, main_question, mission_path, plan: Plan, memory_stream: MemoryStream):
        self.main_question = main_question
        pmission = PromptTemplate(mission_path)
        self.mission = pmission.get_prompt()
        self.plan = plan
        self.memory_stream = memory_stream

    def merge_data(self):
        self.merged_data = dict()
        self.merged_data["DetailedStrategy"] = self.plan.detailed_strategy
        self.merged_data["Plan"] = []
        for entry in self.plan.get_json_data()["Plan"]:
            tmp = copy.deepcopy(entry)
            new_entry = dict()
            new_entry["DocumentID"] = tmp["DocumentID"]
            new_entry["Purpose"] = tmp["Purpose"]
            new_entry["Perspectives"] = tmp["Perspectives"]
            #print(new_entry)
            if isinstance(entry["ResultID"], int) or isinstance(entry["ResultID"], float):
                if entry["ResultID"] >= 0:
                    data = self.memory_stream.get_data(entry["ResultID"])
                    #print(data)
                    new_entry["ResultID"] = { "Reply": data["Reply"], "Point": data["Point"] }
                else:
                    new_entry["ResultID"] = { "Reply": "No Reply", "Point": 0.0 }
            else:
                    new_entry["ResultID"] = { "Reply": "No Reply", "Point": 0.0 }
            self.merged_data["Plan"].append(new_entry)
        #print(merged_data)
        with open("./test/result/plan_result.json", "w", encoding="utf-8") as f:
            json.dump(self.merged_data, f, indent=4, ensure_ascii=False)

    def evaluate(self, template_path):
        self.merge_data()
        temp = PromptTemplate(template_path)
        prompt = temp.get_prompt(
            MainQuestion = self.main_question,
            Mission = self.mission,
            PastStrategies = [],
            PlanExecutedResults = self.merged_data
        )
        reply = get_response(prompt)
        print(reply)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: <MainQuestion> <plan> <memory>")
        sys.exit(1)
    main_question = sys.argv[1]
    plan_json_path = sys.argv[2]
    mem_json_path = sys.argv[3]
    plan = Plan()
    plan.load_from_json(plan_json_path)
    mission_path= "./prompt_templates/ptemplate_mission.txt"
    memory_stream = MemoryStream()
    memory_stream.load_from_json(mem_json_path)
    evaluator = Evaluator(main_question, mission_path, plan, memory_stream)
    evaluator.evaluate("./prompt_templates/ptemplate_evaluate.txt")