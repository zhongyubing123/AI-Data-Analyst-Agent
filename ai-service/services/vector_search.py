from pathlib import Path
import pickle
import logging

import faiss
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


VECTOR_DIR = (
    Path(__file__).parent.parent
    / "vector_store"
)


model = None
index = None
documents = None



def load_vector_store():

    global model
    global index
    global documents


    if model is None:

        logger.info(
            "Loading embedding model"
        )

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )



    if index is None:

        logger.info(
            "Loading FAISS index"
        )

        index = faiss.read_index(
            str(
                VECTOR_DIR
                / "index.faiss"
            )
        )



    if documents is None:

        logger.info(
            "Loading documents"
        )

        with open(
            VECTOR_DIR / "docs.pkl",
            "rb"
        ) as f:

            documents = pickle.load(f)



def search(
    query: str,
    top_k: int = 3
):

    """
    检索知识库
    """


    load_vector_store()



    embedding = model.encode(
        [query]
    )



    _, indexes = index.search(
        embedding,
        top_k
    )



    return [

        documents[i]

        for i in indexes[0]

        if 0 <= i < len(documents)

    ]