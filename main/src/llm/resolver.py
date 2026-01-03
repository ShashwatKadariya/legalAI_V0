from sentence_transformers import SentenceTransformer
import numpy as np
from parsing.regex import SUBSECTION_RE_QUERY, SECTION_RE_QUERY, CLAUSE_RE_QUERY

_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

TOP_SCORE_THRESHOLD = 0.55
MARGIN_THRESHOLD = 0.08

INTENT_PROTOTYPES = {
    "SYMBOLIC": [
        "list legal provisions",
        "show sections and clauses",
        "exact legal lookup",
        "which clauses are included",
        "के के छन्",
        "दफा के के",
    ],
    "SEMANTIC": [
        "explain the meaning of the law",
        "what is the intent of this provision",
        "interpret this section",
        "why does the law say this",
        "उद्देश्य के हो",
        "व्याख्या गर्नु",
    ],
}

_PROTOTYPE_EMBEDS = {
    intent: _MODEL.encode(texts, normalize_embeddings=True)
    for intent, texts in INTENT_PROTOTYPES.items()
}


def has_section_reference(text: str) -> bool:
    return bool(SECTION_RE_QUERY.search(text))


def has_clause_reference(text: str) -> bool:
    return bool(CLAUSE_RE_QUERY.search(text))


def llm_detect_intent(query: str) -> str:
    """
    Lightweight intent classifier using embedding similarity.
    Returns: 'SYMBOLIC' or 'SEMANTIC'
    """

    q_emb = _MODEL.encode([query], normalize_embeddings=True)[0]

    scores = {}

    for intent, embeds in _PROTOTYPE_EMBEDS.items():
        # Max similarity to any prototype of that intent
        sim = np.max(np.dot(embeds, q_emb))
        scores[intent] = sim

    # Pick best intent
    return max(scores, key=scores.get)
