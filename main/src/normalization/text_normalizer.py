import re

NEPALI_TO_ASCII_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

correction_map = {
    "पररच्िेद": "पररच्छेद",
    "पररच्छेय": "पररच्छेद",
}


def correct_common_errors(text):
    corrected = text
    for wrong, right in correction_map.items():
        corrected = corrected.replace(wrong, right)
    return corrected


def normalize_digits(text):
    return text.translate(NEPALI_TO_ASCII_DIGITS)


def normalize_whitespace(text):
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_clause_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r'[\uf000-\uf0ff]', '', text)
    return text

