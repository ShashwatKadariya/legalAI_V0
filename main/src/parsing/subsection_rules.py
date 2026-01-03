def is_structural_subsection(text, match_start):
    before = text[max(0, match_start - 10):match_start]

    if "उपदफा" in before:
        return False

    after = text[match_start:match_start + 20]
    if "," in after or "वा" in after:
        return False

    return True
