from llm.call_llm import call_llm
from llm.conversation.state import ConversationState
from models.citation import build_citations
from retrieval.context_builder import build_context
from retrieval.retrieve_semantic import retrieve_semantic
from llm.prompts.legal_answer_prompt import legal_answer_prompt
from normalization.text_normalizer import normalize_digits


def answer_query(query: str, state: ConversationState, k: int = 8):
    state.add_user(query)

    standalone_query = normalize_digits(query)
    print("Query:", standalone_query)
    print("STATE", state)
    units = retrieve_semantic(
        query=standalone_query,
        act=state.act,
        chapter=state.chapter,
        section=state.section,
        k=k
    )

    if not units:
        answer = "यस प्रश्नको उत्तर प्रदान गरिएको कानूनी सन्दर्भमा स्पष्ट रूपमा उल्लेख छैन।"
        state.add_assistant(answer)
        return {
            "answer": answer,
            "citations": []
        }

    best = units[0]
    state.act = best.act
    state.chapter = best.chapter
    state.section = best.section

    context = build_context(units)

    prompt = legal_answer_prompt.format(context, standalone_query)
    answer = call_llm(prompt)

    NOT_FOUND_MSG = "यस प्रश्नको उत्तर यस ऐनमा स्पष्ट रूपमा छैन।"



    state.add_assistant(answer)

    if answer.strip() == NOT_FOUND_MSG:
        citations = []
    else:
        citations = build_citations(units)

    return {
        "answer": answer,
        "potential_citations": citations
    }

