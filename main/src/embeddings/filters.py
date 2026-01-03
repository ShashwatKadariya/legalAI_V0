from typing import Dict


def prepare_embedding_text(record):
    return f"passage: {record['text'].strip()}"


def should_embed(record: Dict) -> bool:
    if record["type"] == "clause":
        return True
    if record["type"] == "subsection" and record["path_ids"]["clause"] is None:
        return True
    return False
