import hashlib
from models.CLAUSE_ROMAN import CLAUSE_ROMAN
from normalization.text_normalizer import normalize_clause_text


def romanize_clause(label):
    if not label:
        return "na"
    return CLAUSE_ROMAN.get(label, label)


def stable_id(prefix: str, text: str, length=12) -> str:
    normalized = normalize_clause_text(text)
    h = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:length]
    return f"{prefix}_{h}"


def build_clause_id(block: dict) -> str:

    pid = block["path_ids"]
    pit = block["path_titles"]

    return (
        f"{stable_id("act", pit['act'])}"
        f"_ch_{pid['chapter'] or 'na'}"
        f"_sec_{pid['section']}"
        f"_sub_{pid['subsection'] or 'na'}"
        f"_cl_{romanize_clause(pid['clause'])}"
    )
