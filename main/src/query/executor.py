from query.structural_lookup import lookup_clause, lookup_section_children, lookup_subsection


def semantic_fallback(plan, meta, index, model, k=5):
    q = f"query: {plan['original_query']}"
    q_emb = model.encode([q], normalize_embeddings=True)
    D, I = index.search(q_emb, k)
    return [meta[i] for i in I[0]]


def execute_query(plan, meta, index, model):
    c = plan["constraints"]

    if c["clause"]:
        res = lookup_clause(meta, c["section"], c["subsection"], c["clause"])
        if res:
            return res

    if c["subsection"]:
        res = lookup_subsection(meta, c["section"], c["subsection"])
        if res:
            return res

    if c["section"]:
        res = lookup_section_children(meta, c["section"])
        if res:
            return res

    return semantic_fallback(plan, meta, index, model)
