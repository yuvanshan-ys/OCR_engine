def detect_category(text):
    text_lower = text.lower()

    if "system design" in text_lower or "scalability" in text_lower:
        return "System Design"
    elif "transformer" in text_lower or "machine learning" in text_lower or "llm" in text_lower:
        return "AI/ML"
    elif "big o" in text_lower or "leetcode" in text_lower or "two pointer" in text_lower:
        return "Interview Prep"
    elif "export" in text_lower or "hs code" in text_lower:
        return "Export/Trade"
    else:
        return "Uncategorized"
