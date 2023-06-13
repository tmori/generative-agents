#!/usr/bin/python
# -*- coding: utf-8 -*-

from question import get_response
from prompt_template import PromptTemplate
import json

class CriticalThinking:
    def __init__(self, main_question: str, prompt_template_path: str):
        prompt_template =  PromptTemplate(prompt_template_path)
        self.query = prompt_template.get_prompt(MainQuestion=main_question)

    def create(self):
        print(self.query)
        self.reply_raw = get_response(self.query)


    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(json.loads(self.reply_raw), file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <MainQuestion>")
        sys.exit(1)
    main_question = sys.argv[1]
    think = CriticalThinking(main_question, "./prompt_templates/ptemplate_critical_thinking.txt")
    think.create()
    think.save_to_json("test/result/critical_thinking.json")
