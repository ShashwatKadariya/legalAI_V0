from typing import List
from embeddings.encoder import embed_texts
from embeddings.qdrant_store import get_client, ensure_collection, qdrant_append
from models.frozen_canonical import RetrievalUnit

COLLECTION = "nepali_laws"

def build_embedding_text(u: RetrievalUnit) -> str:
    return (
        f"Act: {u.path_titles.act}\n"
        f"Chapter: {u.path_titles.chapter}\n"
        f"Section: {u.path_titles.section}\n"
        f"Subsection: {u.path_titles.subsection}\n"
        f"Clause: {u.path_titles.clause}\n"
        f"Text: {u.text}"
    )


def index_units(units: List[RetrievalUnit]) -> None:
    texts = [f"passage: {build_embedding_text(u)}" for u in units]
    vectors = embed_texts(texts)

    ensure_collection(len(vectors[0]))
    client = get_client()

    points = []
    for u, v in zip(units, vectors):
        qdrant_append(points, u, v)

    client.upsert(collection_name=COLLECTION, points=points)


