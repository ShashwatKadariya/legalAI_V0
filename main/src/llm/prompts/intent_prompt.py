INTENT_PROMPT = """
    You are a legal query classifier.
    
    Classify the following query into exactly ONE category:
    
    SYMBOLIC:
    - asking for exact sections, clauses, subsections
    - asking to list provisions
    - direct legal lookup
    
    SEMANTIC:
    - asking for explanation, meaning, intent, effect
    - interpretation or reasoning
    
    Query:
    "{query}"
    
    Respond with ONLY one word:
    SYMBOLIC or SEMANTIC.
"""