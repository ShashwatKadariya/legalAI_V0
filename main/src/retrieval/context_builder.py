
def build_context(units):
    parts = []

    for u in units:
        parts.append(
            f"""
                [ACT]
                {u.act}
                
                [SECTION]
                {u.section}
                
                [PROVISION TEXT]
                {u.text}
            """.strip()
            )

    return "\n\n---\n\n".join(parts)
