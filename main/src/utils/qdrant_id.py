import uuid
import hashlib


def qdrant_point_id(canonical_id: str) -> str:
    h = hashlib.sha256(canonical_id.encode("utf-8")).hexdigest()
    return str(uuid.UUID(h[:32]))
