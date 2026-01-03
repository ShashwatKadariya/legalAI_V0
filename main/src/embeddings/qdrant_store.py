from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from utils.qdrant_id import qdrant_point_id

COLLECTION = "nepali_laws"


def qdrant_append(points, u, v):
    points.append(
        PointStruct(
            id=qdrant_point_id(u.id),
            vector=v,
            payload={
                "canonical_id": u.id,
                **u.path_ids.model_dump(),
                **u.path_titles.model_dump(),
                "type": u.type,
                "text": u.text,
                "language": u.language
            }
        )
    )

def get_client():
    return QdrantClient(url="http://localhost:6333")


def ensure_collection(dim: int):
    client = get_client()

    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION in collections:
        return

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=dim,
            distance=Distance.COSINE
        )
    )
