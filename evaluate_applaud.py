#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from prompt_template import PromptTemplate
from question import get_response

def do_applaud(name: str, document_path: str, template_path):
    file_list = os.listdir(document_path)
    log_data = ""
    for file in file_list:
        with open(document_path + "/" + file) as file:
            data = file.read()
            log_data += data
    prompt = PromptTemplate(template_path)
    p = prompt.get_prompt(
        Name = name,
        log_data = log_data)
    print(p)
    return get_response(p)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: <name> <document_path> <template_path>")
        sys.exit(1)
    result = do_applaud(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result)
