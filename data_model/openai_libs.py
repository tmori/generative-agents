#!/usr/bin/python
# -*- coding: utf-8 -*-

import openai
import tiktoken
from tiktoken.core import Encoding
from openai.embeddings_utils import cosine_similarity

llm_model = "gpt-4-0613"
embedding_model = "text-embedding-ada-002"

# Embedding
def get_embedding(text_input: str):
    global embedding_model
    
    # ベクトル変換
    response  = openai.Embedding.create(
                    input = text_input.replace("\n", " "),   # 入力文章
                    model = embedding_model,        # GPTモデル
                 )
    
    # 出力結果取得
    embeddings = response['data'][0]['embedding']
    
    return embeddings

def get_score(text1: str, text2: str):
    vec1 = get_embedding(text1)
    vec2 = get_embedding(text2)
    result = cosine_similarity(vec1, vec2)
    return result


def get_tokenlen(data: str):
    encoding: Encoding = tiktoken.encoding_for_model(llm_model)
    tokens = encoding.encode(data)
    return len(tokens)
