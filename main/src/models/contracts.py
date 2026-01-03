from models.canonical_ids import build_clause_id
from models.citation import build_citation
from normalization.text_normalizer import normalize_clause_text


def is_valid_clause(block: dict) -> bool:
    if block.get("type") != "clause":
        return False

    text = normalize_clause_text(block.get("content", ""))
    if len(text) < 5:
        return False

    pt = block.get("path_titles", {})
    required = ["act", "section", "clause"]

    for r in required:
        if not pt.get(r):
            return False

    return True


def build_clause_object(block: dict, source_meta: dict) -> dict:
    clause_text = normalize_clause_text(block["content"])

    return {
        "id": build_clause_id(block),
        "type": "clause",
        "retrieval_unit": True,
        "text": clause_text,
        "path_ids": block["path_ids"],
        "path_titles": block["path_titles"],
        "citation": build_citation(block),
        "source": source_meta,
        "language": "ne"
    }


def build_subsection_object(block, source_meta):
    return {
        "id": build_clause_id(block),
        "type": "subsection",
        "retrieval_unit": True,
        "text": normalize_clause_text(block["content"]),
        "path_ids": block["path_ids"],
        "path_titles": block["path_titles"],
        "citation": build_citation(block),
        "source": source_meta,
        "language": "ne"
    }


def build_section_object(block, source_meta):
    return {
        "id": build_clause_id(block),
        "type": "section",
        "retrieval_unit": True,
        "text": normalize_clause_text(block["content"]),
        "path_ids": block["path_ids"],
        "path_titles": block["path_titles"],
        "citation": build_citation(block),
        "source": source_meta,
        "language": "ne"
    }
