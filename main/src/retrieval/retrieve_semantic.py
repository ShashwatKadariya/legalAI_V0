from typing import List

from qdrant_client.models import Filter, FieldCondition, MatchValue
from embeddings.encoder import embed_texts
from embeddings.qdrant_store import get_client
from models.frozen_canonical import RetrievalUnit, RetrievedUnit


def retrieve_semantic(
        query: str,
        *,
        score_threshold=0.32,
        act: str | None = None,
        chapter: str | None = None,
        section: str | None = None,
        k: int = 8
) -> list[RetrievedUnit]:

    client = get_client()
    vector = embed_texts([f"query: {query}"])[0]

    must = []

    if act:
        must.append(FieldCondition(key="act", match=MatchValue(value=act)))

    if chapter:
        must.append(FieldCondition(key="chapter", match=MatchValue(value=chapter)))

    if section:
        must.append(FieldCondition(key="section", match=MatchValue(value=section)))

    results = client.query_points(
        collection_name="nepali_laws",
        query=vector,
        limit=k,
        with_payload=True,
        score_threshold=score_threshold,
        query_filter=Filter(must=must)
    )

    # return [RetrievalUnit.from_payload(p.payload) for p in results.points]
    return [
        RetrievedUnit(
            id=p.payload["canonical_id"],
            **{k: v for k, v in p.payload.items() if k != "canonical_id"}
        )
        for p in results.points
    ]

