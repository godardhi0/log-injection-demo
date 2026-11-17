def sanitize_for_log(value: str, max_length: int = 100) -> str:
    """Makes a user value safe to write in a log (CWE-117).

    Line breaks are replaced by visible text (\\n and \\r).
    The evidence of the attack stays readable, but the value can no longer
    create a new line in the file.
    """
    value = value.replace("\r", "\\r").replace("\n", "\\n")
    if len(value) > max_length:
        value = value[:max_length] + "...[tronqué]"
    return value