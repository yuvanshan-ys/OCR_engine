import re

def extract_links(text):
    link_pattern = r"https?://[^\s]+"
    return re.findall(link_pattern, text)
