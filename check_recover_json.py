#!/usr/bin/python
# -*- coding: utf-8 -*-

from question import get_response
from json_utils import parse_json
import json
import traceback

def check_json_str(json_data: str):
    try:
        _ = json.loads(json_data)
        return (True, "OK")
    except json.JSONDecodeError as e:
        traceback_str = traceback.format_exc()
        error_message = f"ERROR: {str(e)}"
        print(traceback_str + error_message)
        return (False, error_message)

def check_json(filepath: str):
    try:
        with open(filepath, "r") as file:
            json_data = json.load(file)
        return (True, "OK")
    except json.JSONDecodeError as e:
        traceback_str = traceback.format_exc()
        error_message = f"ERROR: {str(e)}"
        print(traceback_str + error_message)
        return (False, error_message)

def recover_json_str(errcode, data: str):
    res = get_response(f"{errcode}\nPlease fix this json data:\n {data}")
    json_data = parse_json(res)
    return json_data

def recover_json(errcode, filepath: str):
    with open(filepath, "r") as file:
        data = file.read()
        json_data = recover_json_str(errcode, data)
        result, _ = check_json_str(json_data)
        return (result, json_data)



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    result, errcode = check_json(filepath)
    if result == False:
        result, json_data = recover_json(errcode, filepath)
        if result == True:
            with open(filepath, "w") as file:
                file.write(json_data)
            sys.exit(0)
        else:
            print("ERROR: can not recover json file", filepath)
            sys.exit(1)
