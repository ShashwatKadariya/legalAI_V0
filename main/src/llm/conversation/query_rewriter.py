from llm.call_llm import call_llm
from llm.conversation.state import ConversationState
from llm.prompts.query_rewrite_prompt import QUERY_REWRITE_PROMPT


def rewrite_query(query: str, state: ConversationState) -> str:
    if not state.turns:
        return query

    history = "\n".join(
        f"{t.role.upper()}: {t.content}"
        for t in state.last_n()
    )

    prompt = QUERY_REWRITE_PROMPT.format(
        history=history,
        query=query
    )

    rewritten = call_llm(prompt)

    # safety fallback
    return rewritten.strip() or query
