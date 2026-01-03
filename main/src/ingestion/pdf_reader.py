import pdfplumber
from normalization.text_normalizer import correct_common_errors

LINE_Y_THRESHOLD = 4.5


def extract_lines(pdf_path: str) -> list[dict]:
    lines = []
    with pdfplumber.open(pdf_path, unicode_norm='NFC') as act_pdf:
        for page_num, page in enumerate(act_pdf.pages, start=1):
            words = page.extract_words(
                use_text_flow=True,
                keep_blank_chars=False
            )
            current_line = []
            current_top = None

            for w in words:
                if current_top is None:
                    current_top = w["top"]

                if abs(w["top"] - current_top) > LINE_Y_THRESHOLD:
                    line_text = " ".join(word["text"] for word in current_line)
                    line_text = correct_common_errors(line_text)
                    lines.append({
                        "text": line_text,
                        "x0": min(word["x0"] for word in current_line),
                        "top": current_top,
                        "page": page_num
                    })
                    current_line = []
                    current_top = w["top"]

                current_line.append(w)

            if current_line:
                line_text = " ".join(word["text"] for word in current_line)
                line_text = correct_common_errors(line_text)
                lines.append({
                    "text": line_text,
                    "x0": min(word["x0"] for word in current_line),
                    "top": current_top,
                    "page": page_num
                })
    return lines