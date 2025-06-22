import re
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # for consistent result
from prefect import task

QUESTION_WORDS = [
    "what", "who", "when", "where", "why", "how", "which", "whom", "whose"
]
# Simple verb list for English (could be expanded or use spaCy for POS tagging)
COMMON_VERBS = [
    "is", "are", "do", "does", "can", "could", "should", "would", "will", "have", "has", "had", "make", "get", "find", "explain", "show", "give", "tell", "list", "compare", "define", "describe"
]
GREETINGS = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night']

@task
def is_valid_natural_language_query(query: str) -> bool:
    if query == 'hi' or query == 'hello':
        return True
    if not isinstance(query, str):
        return False
    query = query.strip()
    # lowercase the query
    query = query.lower()
    if len(query) < 3 and query != 'hi':
        return False
    # Remove excessive whitespace
    query = re.sub(r'\s+', ' ', query)
    # Must have at least 2 words
    words = query.split()
    if len(words) < 2:
        return False
    # Must contain at least one alphabetic character
    if not re.search(r'[A-Za-zÀ-ỹ]', query):
        return False
    # Reject if too many special characters
    special_ratio = len(re.findall(r'[^A-Za-zÀ-ỹ0-9\s]', query)) / max(1, len(query))
    if special_ratio > 0.4:
        return False
    # Reject if mostly numbers
    num_ratio = len(re.findall(r'[0-9]', query)) / max(1, len(query))
    if num_ratio > 0.7:
        return False
    # Check for question words or common verbs
    q_lower = query.lower()
    if not any(qw in q_lower for qw in QUESTION_WORDS + COMMON_VERBS + GREETINGS):
        return False
    # Reject if all words are the same (e.g., "hello hello hello")
    if len(set(words)) == 1:
        return False
    # Optionally: reject if no punctuation at end (for stricter validation)
    # if not re.search(r'[.?!]$', query):
    #     return False
    return True

@task
def detect_language(query: str) -> str:
    try:
        return detect(query)
    except:
        return "unknown"