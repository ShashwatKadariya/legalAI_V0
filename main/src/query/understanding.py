from typing import Optional, Dict
import re
from config.embeddings import STRUCTURAL_WORDS, ENUM_WORDS, ENUM_SUFFIXES


def normalize_query(q: str) -> str:
    return q.lower().strip()


def extract_section(q: str) -> Optional[str]:
    m = re.search(r"(?:दफा|धारा|section)\s*(\d+)", q)
    return m.group(1) if m else None


def extract_subsection(q: str) -> Optional[str]:
    m = re.search(r"(?:उपदफा|subsection)\s*\(?(\d+)\)?", q)
    return m.group(1) if m else None


def extract_clause(q: str) -> Optional[str]:
    m = re.search(r"(?:खण्ड|clause)\s*\(?([क-ह])\)?", q)
    return m.group(1) if m else None


def detect_intent(q: str) -> str:
    if any(w in q for w in STRUCTURAL_WORDS):
        return "STRUCTURAL"
    if extract_section(q) and (
            any(w in q for w in ENUM_WORDS) or
            any(sfx in q for sfx in ENUM_SUFFIXES)
    ):
        return "ENUMERATION"
    if extract_section(q):
        return "PROVISION_LOOKUP"
    return "INTERPRETIVE"


def build_query_plan(query: str) -> Dict:
    qn = normalize_query(query)
    return {
        "original_query": query,
        "intent": detect_intent(qn),
        "constraints": {
            "section": extract_section(qn),
            "subsection": extract_subsection(qn),
            "clause": extract_clause(qn)
        }
    }
