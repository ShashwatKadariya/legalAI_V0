from pipeline.answer import answer_query
from llm.conversation.state import ConversationState

state = ConversationState()

while True:
    query = input("\nUser> ").strip()
    if query.lower() in {"exit", "quit"}:
        break

    result = answer_query(query, state)
    print("\nAssistant>", result["answer"])

    if result.get("potential_citations"):
        print("Citations:")
        for c in result["potential_citations"]:
            print(" -", c)

