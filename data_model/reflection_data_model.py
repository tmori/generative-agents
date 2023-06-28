#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

from data_model import DataModel

class ReflectionDataModel:
    def __init__(self, term: str):
        self.term = term
        self.known_infos = []
        self.relations = []

    def add_info(self, known_info: str, document_ids: list):
        data = {
            "KnownInfo": known_info,
            "DocumentIDs": document_ids
        }
        if all(data.get("KnownInfo") != entry.get("KnownInfo") for entry in self.known_infos):
            self.known_infos.append(data)

    def get_known_infos_num(self):
        return len(self.known_infos)


    def add_relations(self, relations):
        self.relations += relations

    def get_term(self) -> str:
        return self.term
    
    def get_contents(self):
        data = {
            "KnownInfos": self.known_infos,
            "Relations": self.relations
        }
        return data

    def get_model(self) -> DataModel:
        return DataModel(self.get_term(), self.get_contents())
    