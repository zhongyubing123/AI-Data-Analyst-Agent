from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

VECTOR_DIR = Path(__file__).parent.parent / "vector_store"

# 加载模型和向量库
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(str(VECTOR_DIR / "index.faiss"))

with open(VECTOR_DIR / "docs.pkl", "rb") as f:
    documents = pickle.load(f)


def search(query: str, top_k: int = 3):
    """
    检索与问题最相关的知识块
    """
    embedding = model.encode([query])
    _, indexes = index.search(embedding, top_k)

    return [
        documents[i]
        for i in indexes[0]
        if i < len(documents)
    ]