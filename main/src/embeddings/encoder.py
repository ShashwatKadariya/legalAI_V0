from typing import List
from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: List[str]):
    model = get_model()
    return model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=16,
        show_progress_bar=True
    )
