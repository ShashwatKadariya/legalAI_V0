from qdrant_client.models import Filter, FieldCondition, MatchValue
from embeddings.qdrant_store import get_client


def retrieve_symbolic(
        *,
        act: str,
        section: str | None = None,
        subsection: str | None = None,
        clause: str | None = None,
):
    client = get_client()

    must = [
        FieldCondition(key="act", match=MatchValue(value=act))
    ]

    if section:
        must.append(FieldCondition(key="section", match=MatchValue(value=section)))
    if subsection:
        must.append(FieldCondition(key="subsection", match=MatchValue(value=subsection)))
    if clause:
        must.append(FieldCondition(key="clause", match=MatchValue(value=clause)))

    results, _ = client.scroll(
        collection_name="nepali_laws",
        scroll_filter=Filter(must=must),
        with_payload=True,
        limit=100
    )

    return results
