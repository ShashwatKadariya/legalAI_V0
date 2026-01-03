def build_citation(block: dict) -> str:
    pt = block["path_titles"]

    parts = [
        pt["act"],
        f"दफा {pt['section'].split('.')[0]}",
    ]

    if pt.get("subsection"):
        parts.append(f"उपदफा {pt['subsection']}")

    if pt.get("clause"):
        parts.append(f"खण्ड ({pt['clause']})")

    return ", ".join(parts)


def build_citations(units):
    seen = set()
    citations = []

    for u in units:
        citation = f"{u.act}, {u.section}"
        if citation not in seen:
            seen.add(citation)
            citations.append(citation)

    return citations
