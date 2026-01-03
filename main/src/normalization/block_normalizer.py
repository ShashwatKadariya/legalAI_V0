def normalize_none(v):
    if v in ("None", "", "null"):
        return None
    return v


def normalize_block(block):
    for k in block["path_ids"]:
        block["path_ids"][k] = normalize_none(block["path_ids"][k])
    for k in block["path_titles"]:
        block["path_titles"][k] = normalize_none(block["path_titles"][k])
    return block
