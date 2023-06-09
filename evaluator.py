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
import traceback

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

    def evaluate(self, template_path, ref_json_path):
        with open(ref_json_path, 'r') as file:
            reflection = file.read()
        with open("./test/result/plan_result.json", 'r') as file:
            PlanExecutedResults = file.read()

        temp = PromptTemplate(template_path)
        prompt = temp.get_prompt(
            MainQuestion = self.main_question,
            Mission = self.mission,
            PastStrategies = [],
            PlanExecutedResults = PlanExecutedResults,
            Reflection = reflection
        )
        try:
            reply = get_response(prompt)
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_message = f"ERROR: {str(e)}"
            print(traceback_str + error_message)
            sys.exit(1)
        print(reply)

if __name__ == "__main__":
    import sys
    from params import get_param
    prompt_template_path = get_param("prompt_templates_path")

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: <MainQuestion> <plan> <memory> [<reflection>]")
        sys.exit(1)
    main_question = sys.argv[1]
    mission_path= prompt_template_path + "/ptemplate_mission.txt"
    if len(sys.argv) == 4:
        plan_json_path = sys.argv[2]
        mem_json_path = sys.argv[3]
        plan = Plan()
        plan.load_from_json(plan_json_path)
        memory_stream = MemoryStream()
        memory_stream.load_from_json(mem_json_path)
        evaluator = Evaluator(main_question, mission_path, plan, memory_stream)
        evaluator.merge_data()
    elif len(sys.argv) == 5:
        ref_json_path = sys.argv[4]
        evaluator = Evaluator(main_question, mission_path, None, None)
        evaluator.evaluate(prompt_template_path + "/ptemplate_evaluate.txt", ref_json_path)