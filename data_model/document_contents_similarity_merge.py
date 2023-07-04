#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from question import get_response
from json_utils import parse_json
from check_recover_json import check_json_str, recover_json_str
from document_data_model import DocumentDataModel

def merge_answers_str(data: str):
    res = get_response(f"For the given json data, compare each Answer, and if it matches the following conditions, merge them, otherwise output as is.:\n 1. The content of the Answer is the same meaning. Let's think step by step.:\n {data}")
    json_data = parse_json(res)
    return json_data

def merge_answers_json(filepath: str):
    with open(filepath, "r") as file:
        data = file.read()
        json_data = merge_answers_str(data)
        return json_data

def merge_and_save_answers_json(filepath: str):
    model = DocumentDataModel.load_json_file(filepath)
    if model.get_conents_num() < 2:
        print(f"INFO: SKIP MERGING MODEL: {filepath} info_num={model.get_conents_num()}")
        return
    print("INFO: MERGING MODEL: ", filepath)
    json_data = merge_answers_json(filepath)
    result, errcode = check_json_str(json_data)
    if result == False:
        json_data = recover_json_str(errcode, json_data)
        result, _ = check_json_str(json_data)
        if (result == False):
            print("ERROR: can not recover json_data...")
            return False
    #print(json_data)
    with open(filepath, "w") as file:
        file.write(json_data)
    return True



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    ret = merge_and_save_answers_json(filepath)
    if ret == False:
        sys.exit(1)
    sys.exit(0)
