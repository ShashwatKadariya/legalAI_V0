from state import ConversationState
from retrieval.router import router
from retrieval.context_builder import build_context
from models.citation import build_citations
from llm.call_llm import call_llm


class ConversationManager:
    def ask(self, query: str) -> dict:
        parsed_refs = call_llm(
            query,
        )

        units = router(
            query=query,
            parsed_refs=parsed_refs,
        )

        if not units:
            return {
                "answer": "सम्बन्धित कानूनी व्यवस्था फेला परेन।",
                "citations": []
            }

        context = build_context(units)

        answer = call_llm(
            query
        )

        citations = build_citations(units)

        return {
            "answer": answer,
            "citations": citations
        }
