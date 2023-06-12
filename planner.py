#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import json
from prompt_template import PromptTemplate
from question import get_response
from plan import Plan
import os

class Planner:
    def __init__(self, main_question, mission_path, strategy_path, query_plan_path, strategy_history_path):
        self.main_question = main_question
        self.mission_path = mission_path
        self.strategy_path = strategy_path
        self.query_plan_path = query_plan_path
        self.strategy_history_path = strategy_history_path
        if os.path.exists(strategy_history_path):
            with open(strategy_history_path, 'r') as file:
                self.strategy_history_json = json.load(file)
        else:
            self.strategy_history_json = {}
        self.plan = Plan()

    def generate_query(self, document_list, history):
        pmission = PromptTemplate(self.mission_path)
        self.mission = pmission.get_prompt()

        pstrategy = PromptTemplate(self.strategy_path)
        self.strategy = pstrategy.get_prompt()

        pquery_plan = PromptTemplate(self.query_plan_path)
        past_strategies = []
        if "Strategies" in self.strategy_history_json:
            past_strategies = self.strategy_history_json["Strategies"]

        self.query_plan = pquery_plan.get_prompt(
            MainQuestion = self.main_question,
            Mission = self.mission,
            Strategy = self.strategy,
            DocumentList = document_list,
            History = history,
            PastStrategies = past_strategies
        )
        print(self.query_plan)

    def create_plan(self):
        self.reply_raw = get_response(self.query_plan)
        print(self.reply_raw)
        self.reply_json = json.loads(self.reply_raw)
        self.plan.set_strategy(self.reply_json["DetailedStrategy"])
        if "Strategies" not in self.strategy_history_json:
            self.strategy_history_json["Strategies"] = []
        self.strategy_history_json["Strategies"].append(self.reply_json["DetailedStrategy"])

        for entry in self.reply_json["Plan"]:
            self.plan.add_data(entry["DocumentID"], entry["Purpose"], entry["Perspectives"])

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.reply_json, file, indent=4, ensure_ascii=False)

    def save_strategy_history(self):
        with open(self.strategy_history_path, 'w') as file:
            json.dump(self.strategy_history_json, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: <MainQuestion> <doc_list.txt>")
        sys.exit(1)
    main_question = sys.argv[1]
    batch_size = 100
    with open(sys.argv[2], 'r') as file:
        lines = file.readlines()
        total_list = [line.strip() for line in lines]
        batched_list = [total_list[i:i+batch_size] for i in range(0, len(total_list), batch_size)]
    planner = Planner(
        main_question = main_question,
        mission_path= "./prompt_templates/ptemplate_mission.txt",
        strategy_path= "./prompt_templates/ptemplate_strategy.txt",
        query_plan_path= "./prompt_templates/ptemplate_query_plan.txt",
        strategy_history_path="./test/strategy_history.json"
    )
    for doc_list in batched_list:
        planner.generate_query(doc_list, "")
        planner.create_plan()
        planner.save_to_json("reply.json")
    planner.plan.save_to_json("test/plan.json")
    planner.save_strategy_history()
