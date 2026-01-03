from normalization.block_normalizer import normalize_block
from retrieval.children_index import build_children_index
from models.contracts import build_clause_object, build_section_object, build_subsection_object
from models.frozen_canonical import PathTitles, PathIDs, RetrievalUnit

def has_meaningful_text(text, min_len=10):
    return text and len(text.strip()) >= min_len

def build_retrieval_units(blocks: list, source_meta: dict) -> list:
    units: list[RetrievalUnit] = []
    seen_ids = set()
    children = build_children_index(blocks)

    for block in blocks:
        block = normalize_block(block)
        pid = block["path_ids"]

        raw_unit = None

        if block["type"] == "clause" and has_meaningful_text(block["content"]):
            raw_unit = build_clause_object(block, source_meta)

        elif block["type"] == "subsection":
            key = (
                pid["act"],
                pid["chapter"],
                pid["section"],
                pid["subsection"]
            )
            if children[key]["clauses"]:
                continue

            if not has_meaningful_text(block["content"]):
                continue

            raw_unit = build_subsection_object(block, source_meta)

        elif block["type"] == "section":
            key = (
                pid["act"],
                pid["chapter"],
                pid["section"],
                None
            )
            if children[key]["subsections"] or children[key]["clauses"]:
                continue

            if not has_meaningful_text(block["content"]):
                continue

            raw_unit = build_section_object(block, source_meta)

        else:
            continue

        if raw_unit["id"] in seen_ids:
            continue

        unit = RetrievalUnit(
            id=raw_unit["id"],
            type=raw_unit["type"],
            text=raw_unit["text"],
            path_ids=PathIDs(**raw_unit["path_ids"]),
            path_titles=PathTitles(**raw_unit["path_titles"]),
        )

        seen_ids.add(unit.id)
        units.append(unit)

    for u in units:
        assert u.text and len(u.text.strip()) > 10

    return units


