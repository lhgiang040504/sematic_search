import re

# Compile regex patterns 1 lần (fast)
chitchat_patterns = [
    r"\bhello\b", r"\bhi\b", r"\bhow (are|r) (you|u)\b", r"\bjoke\b", r"\bwhat'?s up\b", r"\bthank you\b"
]

procedural_patterns = [
    r"\bhow to\b", r"\bsteps?\b", r"\bguide\b", r"\bprocess\b", r"\bprocedure\b", r"\bworkflow\b"
]

multi_patterns = [
    r"\bcompare\b", r"\bdifferences?\b", r"\badvantages?\b", r"\bpros? and cons?\b", r"\btop\b", r"\bbest\b"
]

def match_patterns(query: str, patterns: list[str]) -> bool:
    q_lower = query.lower()
    for pattern in patterns:
        if re.search(pattern, q_lower):
            return True
    return False

def is_chitchat_query(query: str) -> bool:
    return match_patterns(query, chitchat_patterns)

def is_procedural_query(query: str) -> bool:
    return match_patterns(query, procedural_patterns)

def is_multi_query(query: str) -> bool:
    return match_patterns(query, multi_patterns)