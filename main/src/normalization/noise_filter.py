import re


def is_noise_line(line):
    text = line["text"]
    x0 = line["x0"]
    page = line["page"]

    if re.match(r"^\d+$", text.strip()) and x0 > 250:
        return True

    if "lawcommission.gov.np" in text:
        return True

    return False
