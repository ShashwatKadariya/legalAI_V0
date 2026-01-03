import re


ACT_RE = re.compile(r"ऐन\s*,\s*[०-९0-9]{4}")
CHAPTER_RE = re.compile(r"(अध्याय|पररच्छेद)\s*[-–]?\s*[०-९0-9]+")
SECTION_RE = re.compile(
    r"(?:दफा\s*)?(?P<num>[०-९0-9]+)[क-ह]?\.\s*(?P<title>[^:(]+)"
)
SUBSECTION_RE = re.compile(r"\(([०-९0-9]+)\)")
CLAUSE_RE = re.compile(r"\(\s*([^\W\d_])\s*\)")



SECTION_RE_QUERY = re.compile(
    r"(?:दफा|section)\s*(\d+)",
    re.IGNORECASE
)

SUBSECTION_RE_QUERY = re.compile(
    r"(?:उपदफा|subsection)\s*\(?(\d+)\)?",
    re.IGNORECASE
)

CLAUSE_RE_QUERY = re.compile(
    r"(?:खण्ड|clause)\s*\(?((?:[क-ह])|(?:[a-h]))\)?",
    re.IGNORECASE
)

CHAPTER_RE_QUERY = re.compile(
    r"(?:परिच्छेद|chapter)\s*[-–]?\s*(\d+)",
    re.IGNORECASE
)

