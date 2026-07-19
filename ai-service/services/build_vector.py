from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
VECTOR_DIR = BASE_DIR / "vector_store"
VECTOR_DIR.mkdir(exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")


documents = []

for file in KNOWLEDGE_DIR.glob("*.md"):
    text = file.read_text(encoding="utf-8")

    documents.extend(
        chunk.strip()
        for chunk in text.split("\n\n")
        if len(chunk.strip()) > 20
    )

print(f"共读取 {len(documents)} 个知识块")

embeddings = model.encode(documents)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, str(VECTOR_DIR / "index.faiss"))

with open(VECTOR_DIR / "docs.pkl", "wb") as f:
    pickle.dump(documents, f)

print("知识库构建完成！")