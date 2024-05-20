import re


def extract_text_between_markers(
    text: str, start_marker: str, end_marker: str
):
    pattern = re.escape(start_marker) + "(.*?)" + re.escape(end_marker)
    matches = re.findall(pattern, text, re.DOTALL)
    return matches
