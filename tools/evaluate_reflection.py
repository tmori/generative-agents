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

    points = []
    for term in json_terms:
        knowns = get_value(json_value, term, "KnownInfos")
        for known in knowns:
            points.append(float(known["Point"]))

    df = pd.DataFrame(points, columns=["Point"])
    ave_num = df["Point"].mean()
    max_num = df["Point"].max()
    min_num = df["Point"].min()

    print("AvePoint:", ave_num, " MaxPoint:", max_num, " MinPointm:", min_num)

    known_lens = []
    for term in json_terms:
        knowns = get_value(json_value, term, "KnownInfos")
        for known in knowns:
            known_lens.append(len(known["KnownInfo"]))

    df = pd.DataFrame(known_lens, columns=["KnownInfo"])
    ave_num = df["KnownInfo"].mean()
    max_num = df["KnownInfo"].max()
    min_num = df["KnownInfo"].min()

    print("AveknwLen:", ave_num, " MaxknwLen:", max_num, " MinknwLen:", min_num)


    relations = []
    for term in json_terms:
        term_relations = get_entry(json_value, term)
        if "Relations" in term_relations:
            #print(term_relations["Relations"])
            relations.append(len(term_relations["Relations"]))

    df = pd.DataFrame(relations, columns=["RelationNum"])
    ave_num = df["RelationNum"].mean()
    max_num = df["RelationNum"].max()
    min_num = df["RelationNum"].min()
    print("AveRelNum:", ave_num, " MaxRelNum:", max_num, " MinRelNum:", min_num)

    unknowns = []
    for term in json_terms:
        terms = get_entry(json_value, term)
        if "UnknownInfo" in terms:
            #print(term_relations["Relations"])
            unknowns.append(len(term_relations["UnknownInfo"]))

    df = pd.DataFrame(unknowns, columns=["UnknownInfo"])
    ave_num = df["UnknownInfo"].mean()
    max_num = df["UnknownInfo"].max()
    min_num = df["UnknownInfo"].min()
    print("AveUnkwnNum:", ave_num, " MaxUnkwnNum:", max_num, " MinUnkwnNum:", min_num)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <reflection_path>")
        sys.exit(1)
    json_path = sys.argv[1]
    evaluate(json_path)
