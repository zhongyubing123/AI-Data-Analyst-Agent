import os

# 模型已缓存在本地，强制离线，避免每次检索都联网校查导致超时
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

"""知识检索：向量检索为主，字符重合度为辅。

all-MiniLM-L6-v2 是英文模型，中文语义区分度一般。知识库只有几块文档，
向量匹配不到时用字符二元组重合度兜底，避免"问得明明有文档却答不知道"。
"""

import logging
import pickle

from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)

VECTOR_DIR = Path(__file__).resolve().parent.parent / "vector_store"

MODEL_NAME = "all-MiniLM-L6-v2"

# 归一化后两条无关文本的 L2 距离大约在 1.2 以上，低于它就认为语义命中
DISTANCE_LIMIT = 1.05

model = None
index = None
documents = None


def load_vector_store():

    global model, index, documents

    if model is None:

        logger.info("加载向量模型")

        model = SentenceTransformer(MODEL_NAME)

    if index is None:

        index = faiss.read_index(str(VECTOR_DIR / "index.faiss"))

    if documents is None:

        with open(VECTOR_DIR / "docs.pkl", "rb") as f:

            documents = pickle.load(f)


def bigrams(text):

    text = "".join(text.split())

    return {text[i:i + 2] for i in range(len(text) - 1)}


def keyword_search(query, top_k):

    """按字符二元组重合度排序，供向量检索失效时兜底。"""

    target = bigrams(query)

    scored = []

    for position, doc in enumerate(documents):

        overlap = len(target & bigrams(doc))

        if overlap:

            scored.append((overlap, position))

    scored.sort(reverse=True)

    return [documents[i] for _, i in scored[:top_k]]


def search(query: str, top_k: int = 3):
    """先用字符重合度排序，一个字都对不上才退回向量检索。

    all-MiniLM-L6-v2 在中文短句上区分度很差，几条文档的向量几乎重合，
    直接用它排序会把同一块内容一直排在最前。知识库规模小，
    字符重合度反而更稳，向量检索保留作兜底。
    """

    load_vector_store()

    ranked = keyword_search(query, top_k)

    if ranked:

        return ranked

    embedding = model.encode([query], normalize_embeddings=True)

    _, indexes = index.search(embedding, top_k)

    return [
        documents[i]
        for i in indexes[0]
        if 0 <= i < len(documents)
    ]
