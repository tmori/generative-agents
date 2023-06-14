#!/usr/bin/python
# -*- coding: utf-8 -*-

from question import get_response
from prompt_template import PromptTemplate
import json
import traceback
import json_utils

class Reflection:
    def __init__(self, main_question: str, knowledge_path: str, plan_result_path: str, prompt_template_path: str, document_list_path: str):
        prompt_template =  PromptTemplate(prompt_template_path)
        with open(knowledge_path, 'r') as file:
            KnowledgesNeeds = file.read()
        with open(plan_result_path, 'r') as file:
            PlanResult = file.read()
        with open(document_list_path, 'r') as file:
            DocumentList = file.read()
        self.query = prompt_template.get_prompt(
            MainQuestion=main_question, 
            KnowledgesNeeds=KnowledgesNeeds,
            PlanResult=PlanResult,
            DocumentList=DocumentList
            )

    def create(self):
        print(self.query)
        try:
            self.reply_raw = get_response(self.query)
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_message = f"ERROR: {str(e)}"
            print(traceback_str + error_message)
            sys.exit(1)
        print(self.reply_raw)

    def save_to_raw(self, file_path):
        with open(file_path, 'w') as file:
            file.write(self.reply_raw)

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(json.loads(self.reply_raw), file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: <MainQuestion> <DocumentList>")
        sys.exit(1)
    main_question = sys.argv[1]
    document_list_path = sys.argv[2]
    think = Reflection(
        main_question, 
        "./test/result/critical_thinking.json",
        "./test/result/plan_result.json",
        "./prompt_templates/ptemplate_reflection.txt",
        document_list_path)
    think.create()
    think.save_to_raw("test/result/reflection.json")
