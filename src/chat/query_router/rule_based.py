import re
import logging
from prefect import task

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Curated patterns
chitchat_patterns = [
    r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgood (morning|evening|afternoon)\b",
    r"\bhow (are|r) (you|u)\b", r"\bhow's it going\b", r"\bwhat'?s up\b", r"\bhow do you do\b",
    r"\bthank(s| you)\b", r"\bplease\b", r"\byou'?re welcome\b",
    r"\btell me a joke\b", r"\bmake me laugh\b", r"\bfunny\b", r"\bhumor\b",
    r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b", r"\btake care\b", r"\blater\b"
]

procedural_patterns = [
    r"\bhow (do|can|would|should|could) (i|we|you)\b", r"\bhow to\b", r"\bwhat\b", r"\bsteps? to\b", r"\bstep by step\b",
    r"\bprocess( to| for)?\b", r"\bprocedure( for)?\b", r"\bworkflow( for)?\b", r"\bguide( to| for)?\b",
    r"\binstructions? for\b", r"\btutorial\b", r"\bwalkthrough\b", r"\bdemonstration\b", r"\bexample of\b",
    r"\bshow me how\b", r"\bwhat is the process for\b", r"\bwhat'?s the best way to\b"
]

multi_patterns = [
    r"\bcompare\b", r"\bcomparison\b", r"\bdifference(s)? between\b", r"\bsimilarities? (and|&) differences?\b",
    r"\bvs\b", r"\bversus\b", r"\btop \\d+\b", r"\bbest [a-z]+s?\b", r"\bmost popular\b", r"\bleading\b",
    r"\brecommended\b", r"\blist of\b", r"\branking\b", r"\bpros? and cons?\b", r"\badvantages? (and|&) disadvantages?\b",
    r"\bbenefits? (and|&) drawbacks?\b", r"\balternatives? to\b", r"\bother options\b", r"\bsimilar to\b"
]

def match_patterns(query: str, patterns: list[str]) -> bool:
    q_lower = query.lower()
    for pattern in patterns:
        if re.search(pattern, q_lower):
            logger.info(f"Pattern matched: '{pattern}' in query: '{query}'")
            return True
    logger.info(f"No pattern matched in query: '{query}'")
    return False

@task
def is_chitchat_query(query: str) -> bool:
    result = match_patterns(query, chitchat_patterns)
    logger.info(f"is_chitchat_query: {result} for query: '{query}'")
    return result

@task
def is_procedural_query(query: str) -> bool:
    result = match_patterns(query, procedural_patterns)
    logger.info(f"is_procedural_query: {result} for query: '{query}'")
    return result

@task
def is_multi_query(query: str) -> bool:
    result = match_patterns(query, multi_patterns)
    logger.info(f"is_multi_query: {result} for query: '{query}'")
    return result