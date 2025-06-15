import re
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # for consistent result

def is_valid_natural_language_query(query: str) -> bool:
    # Check too short
    if len(query) < 3:
        return False
    # Check ratio of alphabet
    alpha_ratio = len(re.findall(r'[A-Za-zÀ-ỹ]', query)) / max(1, len(query))
    if alpha_ratio < 0.5:
        return False
    # Check excessive special characters
    special_ratio = len(re.findall(r'[^A-Za-zÀ-ỹ0-9\s]', query)) / max(1, len(query))
    if special_ratio > 0.4:
        return False
    return True


def detect_language(query: str) -> str:
    try:
        return detect(query)
    except:
        return "unknown"