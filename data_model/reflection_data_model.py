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
        self.unknown_infos = []

    def is_empty(self):
        if len(self.known_infos) == 0 and len(self.unknown_infos) == 0:
            return True
        else:
            return False

    def merge(self, old_model: DataModel):
        # merge KnownInfos
        old_contents = old_model.get_contents()
        if old_contents is None:
            return
        if old_contents.get("KnownInfos") is not None:
            old_known_infos = []
            for old_data in old_contents.get("KnownInfos"):
                if all(old_data.get("KnownInfo") != entry.get("KnownInfo") for entry in self.known_infos):
                    old_known_info = {
                        "KnownInfo": old_data.get("KnownInfo"),
                        "DocumentIDs": old_data.get("DocumentIDs"),
                        "Point": old_data.get("Point")
                    }
                    old_known_infos.append(old_known_info)
            self.known_infos += old_known_infos
        
        # merge Relations
        if old_contents.get("Relations") is not None:
            old_relations = []
            for old_data in old_contents.get("Relations"):
                if all(old_data.get("Term") != entry.get("Term") for entry in self.relations):
                    old_relations.append(old_data)
            
            self.relations += old_relations

    def add_info(self, known_info: str, document_ids: list, point: float):
        if len(known_info) == 0:
            return
        if document_ids is None or len(document_ids) == 0:
            #unreliable info
            return
        if not isinstance(point, float) or float(point) < 60.0:
            #unreliable info
            return
        data = {
            "KnownInfo": known_info,
            "DocumentIDs": document_ids,
            "Point": point
        }
        if all(data.get("KnownInfo") != entry.get("KnownInfo") for entry in self.known_infos):
            self.known_infos.append(data)

    def update_unknown_info(self, unknwon_infos: list):
        self.unknown_infos = unknwon_infos

    def get_known_infos_num(self):
        return len(self.known_infos)


    def add_relations(self, relations):
        self.relations += relations

    def get_term(self) -> str:
        return self.term
    
    def get_contents(self):
        if self.is_empty():
            return None
        data = {
            "Term": self.term,
            "KnownInfos": self.known_infos,
            "UnknownInfo": self.unknown_infos,
            "Relations": self.relations
        }
        return data
    def get_known_infos(self):
        if self.known_infos == None:
            return []
        return self.known_infos
    
    def is_empty_content(self):
        if len(self.known_infos) == 0:
            return True
        else:
            return False

    def get_model(self) -> DataModel:
        data_model = DataModel(self.get_term(), self.get_contents())
        data_model.set_concrete_model(self)
        return data_model

    @staticmethod
    def create_from_entry(name: str, entry: dict):
        model = ReflectionDataModel(name)
        if entry is not None and entry.get("KnownInfos") is not None:
            for known_info in entry.get("KnownInfos"):
                model.add_info(known_info.get("KnownInfo"), known_info.get("DocumentIDs"), known_info.get("Point"))
            if entry.get("Relations") is not None:
                model.add_relations(entry.get("Relations"))
            if entry.get("UnknownInfo") is not None:
                model.update_unknown_info(entry.get("UnknownInfo"))
            if entry.get("Point") is not None:
                model.point = entry.get("Point")
        return model
    
    @staticmethod
    def load_json_file(filepath: str):
        data_model = DataModel.load_json_file(filepath)
        if data_model == None:
            return None
        model = ReflectionDataModel.create_from_entry(
                    data_model.get_name(), 
                    data_model.get_contents())
        return model
