#!/usr/bin/python
# -*- coding: utf-8 -*-

from prompt_template import PromptTemplate
from question import get_response

def evaluate_results(query_path: str, result1_path: str, result2_path: str, template_path):
    try:
        with open(query_path, 'r') as file:
            query = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{query_path}' not found.")
    try:
        with open(result1_path, 'r') as file:
            result1 = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{result1_path}' not found.")
    try:
        with open(result2_path, 'r') as file:
            result2 = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{result2_path}' not found.")

    prompt = PromptTemplate(template_path)
    p = prompt.get_prompt(
        MainQuestion = query,
        Result1 = result1,
        Result2 = result2)
    print(p)
    return get_response(p)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: <query_path> <result1_path> <result2_path> <template_path>")
        sys.exit(1)
    result = evaluate_results(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print(result)
