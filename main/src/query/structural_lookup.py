def lookup_clause(meta, sec, sub, cl):
    return [
        r for r in meta
        if r["path_ids"]["section"] == sec
        and r["path_ids"]["subsection"] == sub
        and r["path_ids"]["clause"] == cl
    ]


def lookup_subsection(meta, sec, sub):
    return [
        r for r in meta
        if r["path_ids"]["section"] == sec
        and r["path_ids"]["subsection"] == sub
        and r["path_ids"]["clause"] is None
    ]


def lookup_section_children(meta, sec):
    return [
        r for r in meta
        if r["path_ids"]["section"] == sec
        and r["type"] in ("subsection", "clause")
    ]
