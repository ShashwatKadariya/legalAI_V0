from retrieval.retrieve_semantic import retrieve_semantic
from retrieval.retrieve_symbolic import retrieve_symbolic


def router(query, parsed_refs):
    if parsed_refs.is_structural:
        return retrieve_symbolic(**parsed_refs)
    else:
        return retrieve_semantic(query, **parsed_refs)
