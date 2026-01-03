from collections import defaultdict


def build_children_index(blocks):
    children = defaultdict(lambda: {
        "clauses": [],
        "subsections": []
    })

    for b in blocks:
        pid = b["path_ids"]

        if b["type"] == "clause":
            key = (
                pid["act"],
                pid["chapter"],
                pid["section"],
                pid["subsection"]
            )
            children[key]["clauses"].append(b)

        elif b["type"] == "subsection":
            key = (
                pid["act"],
                pid["chapter"],
                pid["section"],
                None
            )
            children[key]["subsections"].append(b)

    return children