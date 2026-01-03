import re

from parsing.regex import ACT_RE, CHAPTER_RE, SECTION_RE, SUBSECTION_RE, CLAUSE_RE
from parsing.state import current, start_block, build_path_ids, build_path_titles, reset_below
from parsing.subsection_rules import is_structural_subsection

from normalization.noise_filter import is_noise_line
from normalization.text_normalizer import normalize_digits, normalize_whitespace


def parse_blocks(lines: list[dict]) -> list[dict]:
    blocks = []
    current_block = None

    def append(text):
        nonlocal current_block
        if current_block and text.strip():
            current_block["content"] += text.strip() + " "



    normalized_lines = []

    for line in lines:
        if is_noise_line(line):
            continue  # skip noise

        text = normalize_digits(line["text"])
        text = normalize_whitespace(text)

        normalized_lines.append({
            "text": text,
            "x0": line["x0"],
            "top": line["top"],
            "page": line["page"]
        })

    for line in normalized_lines:
        text = line["text"]
        page = line.get("page")

        if ACT_RE.search(text) and page == 1 and current["act"] is None:
            year = re.search(r"[०-९0-9]{4}", text).group()

            current_block = start_block("act", number=year, title=text)
            current["act"] = current_block
            current_block["path_ids"] = build_path_ids()
            current_block["path_titles"] = build_path_titles()

            blocks.append(current_block)
            reset_below("act")
            continue

        chap = CHAPTER_RE.search(text)
        if chap:
            num = re.search(r"[०-९0-9]+", chap.group()).group()

            reset_below("act")

            current_block = start_block("chapter", number=num, title=chap.group())
            current["chapter"] = current_block
            current_block["path_ids"] = build_path_ids()
            current_block["path_titles"] = build_path_titles()

            blocks.append(current_block)

            reset_below("chapter")
            text = text[chap.end():]

        sec = SECTION_RE.search(text)
        if sec and current["chapter"]:
            sec_num = sec.group(1)
            sec_title = sec.group("title").strip()
            reset_below("chapter")

            current_block = start_block("section", number=sec_num, title=sec_title)
            current["section"] = current_block
            current_block["path_ids"] = build_path_ids()
            current_block["path_titles"] = build_path_titles()

            blocks.append(current_block)
            text = text[sec.end():]

        pos = 0
        while pos < len(text):
            sub = SUBSECTION_RE.search(text, pos)
            cl = CLAUSE_RE.search(text, pos)

            next_token = None
            if sub and (not cl or sub.start() < cl.start()):
                next_token = ("subsection", sub)
            elif cl:
                next_token = ("clause", cl)

            if not next_token:
                append(text[pos:])
                break

            token_type, match = next_token
            append(text[pos:match.start()])

            if token_type == "subsection":
                if not is_structural_subsection(text, match.start()):
                    append(match.group())
                    pos = match.end()
                    continue

                num = match.group(1)

                if current["clause"] is None:
                    reset_below("section")
                else:
                    reset_below("clause")

                current_block = start_block("subsection", number=num, title=f"({num})")
                current["subsection"] = current_block
                current_block["path_ids"] = build_path_ids()
                current_block["path_titles"] = build_path_titles()

                blocks.append(current_block)

            else:
                label = match.group(1)

                reset_below("section")

                current_block = start_block("clause", label=label)
                current["clause"] = current_block
                current_block["path_ids"] = build_path_ids()
                current_block["path_titles"] = build_path_titles()

                blocks.append(current_block)

            pos = match.end()
    return blocks
