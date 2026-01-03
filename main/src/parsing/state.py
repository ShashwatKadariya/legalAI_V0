current = {
    "act": None,
    "chapter": None,
    "section": None,
    "subsection": None,
    "clause": None
}


def start_block(block_type, **kwargs):
    return {
        "type": block_type,
        **kwargs,
        "content": "",
        "path": None
    }


def reset_below(level):
    order = ["act", "chapter", "section", "subsection", "clause"]
    idx = order.index(level)
    for k in order[idx + 1:]:
        current[k] = None


def build_path():
    return {
        "act": current["act"]["number"] if current["act"] else None,
        "chapter": current["chapter"]["number"] if current["chapter"] else None,
        "section": current["section"]["number"] if current["section"] else None,
        "subsection": current["subsection"]["number"] if current["subsection"] else None,
        "clause": current["clause"]["label"] if current["clause"] else None,
    }


def build_path_ids():
    return {
        "act": current["act"]["number"] if current["act"] else None,
        "chapter": current["chapter"]["number"] if current["chapter"] else None,
        "section": current["section"]["number"] if current["section"] else None,
        "subsection": current["subsection"]["number"] if current["subsection"] else None,
        "clause": current["clause"]["label"] if current["clause"] else None,
    }


def build_path_titles():
    return {
        "act": current["act"]["title"] if current["act"] else None,
        "chapter": current["chapter"]["title"] if current["chapter"] else None,
        "section": (
            f"{current['section']['number']}. {current['section']['title']}"
            if current["section"] else None
        ),
        "subsection": (
            current["subsection"]["title"] if current["subsection"] else None
        ),
        "clause": current["clause"]["label"] if current["clause"] else None,
    }
