#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from deepdiff import DeepDiff
import jsondiff
import pandas as pd

def get_value(json: dict, term: str, key: str):
    for entry in json["Knowledges"]:
        if term == entry["Term"]:
            return entry[key]

def get_entry(json: dict, term: str):
    for entry in json["Knowledges"]:
        if term == entry["Term"]:
            return entry


def evaluate(json_path: str):
    with open(json_path, 'r') as file:
        json_data = file.read()

    json_value = json.loads(json_data)
    #print(json_value)
    json_terms = []
    for entry in json_value["Knowledges"]:
        json_terms.append(entry["Term"])
    
    print("TermNum: ", len(json_terms))
    knowns = []
    for term in json_terms:
        known = get_value(json_value, term, "KnownInfos")
        knowns.append(len(known))

    df = pd.DataFrame(knowns, columns=["KnownInfos"])
    ave_num = df["KnownInfos"].mean()
    max_num = df["KnownInfos"].max()
    min_num = df["KnownInfos"].min()

    print("AveKnwNum:", ave_num, " MaxKnwNum:", max_num, " MinKnwNum:", min_num)

    docnums = []
    for term in json_terms:
        knowns = get_value(json_value, term, "KnownInfos")
        for known in knowns:
            term_docids = known["DocumentIDs"]
            docnums.append(len(term_docids))

    df = pd.DataFrame(docnums, columns=["DocNum"])
    ave_num = df["DocNum"].mean()
    max_num = df["DocNum"].max()
    min_num = df["DocNum"].min()

    print("AveDocNum:", ave_num, " MaxDocNum:", max_num, " MinDocNum:", min_num)

    relations = []
    for term in json_terms:
        term_relations = get_entry(json_value, term)
        relations.append(len(term_relations))

    df = pd.DataFrame(relations, columns=["RelationNum"])
    ave_num = df["RelationNum"].mean()
    max_num = df["RelationNum"].max()
    min_num = df["RelationNum"].min()
    print("AveRelNum:", ave_num, " MaxRelNum:", max_num, " MinRelNum:", min_num)



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <reflection_path>")
        sys.exit(1)
    json_path = sys.argv[1]
    evaluate(json_path)
