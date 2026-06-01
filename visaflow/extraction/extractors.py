import re
from typing import Dict, List


MONTH_PATTERN = r"(January|February|March|April|May|June|July|August|September|October|November|December)"
DATE_PATTERN = rf"{MONTH_PATTERN}\s+\d{{1,2}}(?:,\s+\d{{4}})?"

ABSOLUTE_DEADLINE_PATTERNS = [
    rf"\bby\s+({DATE_PATTERN})",
    rf"\bdue\s+(?:on\s+)?({DATE_PATTERN})",
    rf"\bsubmit(?:ted)?\s+(?:on|by)\s+({DATE_PATTERN})",
]

RELATIVE_DEADLINE_PATTERNS = [
    r"\bwithin\s+\d+\s+business\s+days\b",
    r"\bwithin\s+\d+\s+days\b",
]


def extract_deadlines(text: str) -> List[str]:
    deadlines = []

    for pattern in ABSOLUTE_DEADLINE_PATTERNS:
        for match in re.findall(pattern, text, flags=re.IGNORECASE):
            if isinstance(match, tuple):
                match = match[0]
            deadlines.append(match.strip())

    for pattern in RELATIVE_DEADLINE_PATTERNS:
        for match in re.findall(pattern, text, flags=re.IGNORECASE):
            deadlines.append(match.strip())

    seen = set()
    ordered = []
    for item in deadlines:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            ordered.append(item)

    return ordered


def extract_requested_documents(text: str) -> List[str]:
    lines = text.splitlines()
    documents = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            documents.append(stripped[2:].strip())

    return documents


def extract_action_items(text: str) -> List[str]:
    actions = []
    patterns = [
        r"\bplease submit\b",
        r"\bplease upload\b",
        r"\breply to this email\b",
        r"\bcheck the .*? portal\b",
        r"\brespond to any follow-up requests\b",
    ]

    lowered = text.lower()
    for pattern in patterns:
        for match in re.finditer(pattern, lowered):
            actions.append(match.group(0))

    seen = set()
    ordered = []
    for item in actions:
        if item not in seen:
            seen.add(item)
            ordered.append(item)

    return ordered


def extract_information(text: str) -> Dict[str, List[str]]:
    return {
        "deadlines": extract_deadlines(text),
        "requested_documents": extract_requested_documents(text),
        "action_items": extract_action_items(text),
    }
