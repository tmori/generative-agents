#!/usr/bin/python
# -*- coding: utf-8 -*-

from document_db import load_db_with_type, similarity_search_with_score
import sys
import pandas as pd


def get_qa(db_dir: str, doc_id: str):
    return load_db_with_type(db_dir + "/" + doc_id)

def get_similarity_search_with_scores(db_dir: str, doc_id: str, terms: str, top_k: int):
    return similarity_search_with_score(db_dir + "/" + doc_id, terms, top_k)

def get_similarity_search_with_average_score(db_dir: str, doc_id: str, terms: str, top_k: int):
    doc_scores = similarity_search_with_score(db_dir + "/" + doc_id, terms, top_k)
    scores = [score[1] for score in doc_scores]
    scores_series = pd.Series(scores, dtype='float64')
    average_score = scores_series.mean()
    return average_score

def get_similarity_search_results(doclist: str, db_dir: str, terms: str, top_k: int):
    with open(doclist, "r") as file:
        lines = file.readlines()
        total_list = [line.strip() for line in lines]

    scores = []
    entries = []
    for entry in total_list:
        score = get_similarity_search_with_average_score(db_dir, entry, terms, top_k)
        scores.append(score)  
        entries.append(entry)
    
    df = pd.DataFrame({'title': entries, 'score': scores})
    top = df.sort_values(by='score', ascending=True).head(top_k)['title'].tolist()
    return top


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("USAGE: " + sys.argv[0] + " <db_dir> <doclist> <terms> <num>")
        sys.exit(1)
    
    db_dir=sys.argv[1]
    doclist=sys.argv[2]
    terms=sys.argv[3]
    num=int(sys.argv[4])

    docs = get_similarity_search_results(doclist, db_dir, terms, num)
    for entry in docs:
        print(entry)
