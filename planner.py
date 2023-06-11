#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import json
from prompt_template import PromptTemplate
from question import get_response
from plan import Plan

class Planner:
    def __init__(self, main_question, mission_path, strategy_path, query_plan_path):
        self.main_question = main_question
        self.mission_path = mission_path
        self.strategy_path = strategy_path
        self.query_plan_path = query_plan_path
        self.plan = Plan()

    def generate_query(self, document_list, history):
        pmission = PromptTemplate(self.mission_path)
        mission = pmission.get_prompt()

        pstrategy = PromptTemplate(self.strategy_path)
        strategy = pstrategy.get_prompt()

        pquery_plan = PromptTemplate(self.query_plan_path)
        self.query_plan = pquery_plan.get_prompt(
            MainQuestion = self.main_question,
            Mission = mission,
            Strategy = strategy,
            DocumentList = document_list,
            History = history
        )
        print(self.query_plan)

    def create_plan(self):
        self.reply_raw = get_response(self.query_plan)
        self.reply_json = json.loads(self.reply_raw)
        for entry in self.reply_json["Plan"]:
            self.plan.add_data(entry["DocumentID"], entry["Purpose"], entry["Perspectives"])

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.reply_json, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: <MainQuestion> <doc_list.txt>")
        sys.exit(1)
    main_question = sys.argv[1]
    with open(sys.argv[2], 'r') as file:
        lines = file.readlines()
        doc_list = [line.strip() for line in lines]
    
    planner = Planner(
        main_question = main_question,
        mission_path= "./prompt_templates/ptemplate_mission.txt",
        strategy_path= "./prompt_templates/ptemplate_strategy.txt",
        query_plan_path= "./prompt_templates/ptemplate_query_plan.txt"
        )
    planner.generate_query(doc_list, "")
    planner.create_plan()
    planner.plan.save_to_json("test/plan.json")
    planner.save_to_json("reply.json")
