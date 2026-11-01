"""构建知识库索引：读 knowledge/*.md，切块、编码、存进 vector_store。

用法（在 ai-service 目录下）：
    python -m services.build_vector

知识文档改过之后必须重跑一次，否则检索到的还是旧内容。
"""

import pickle

from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"

VECTOR_DIR = BASE_DIR / "vector_store"

CHUNK_SIZE = 300

MIN_SIZE = 50

MODEL_NAME = "all-MiniLM-L6-v2"


def split_text(text):

    chunks = []

    for start in range(0, len(text), CHUNK_SIZE):

        piece = text[start:start + CHUNK_SIZE].strip()

        if len(piece) >= MIN_SIZE:

            chunks.append(piece)

    return chunks


def load_docs():

    docs = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):

        text = path.read_text(encoding="utf-8")

        docs.extend(split_text(text))

    return docs


def build():

    docs = load_docs()

    if not docs:

        raise Exception("knowledge 目录下没有可用文档")

    print("知识块 %d 个" % len(docs))

    model = SentenceTransformer(MODEL_NAME)

    # 与 vector_search 保持一致，不归一化
    vectors = np.array(model.encode(docs, normalize_embeddings=True)).astype("float32")

    index = faiss.IndexFlatL2(vectors.shape[1])

    index.add(vectors)

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(VECTOR_DIR / "index.faiss"))

    with open(VECTOR_DIR / "docs.pkl", "wb") as f:

        pickle.dump(docs, f)

    print("索引已写入 %s" % VECTOR_DIR)


if __name__ == "__main__":
    build()
