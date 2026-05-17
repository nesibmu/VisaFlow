import re
from dateutil import parser
from visaflow.schemas import ActionItem, Deadline, ExtractionResult, RequestedDocument


MONTH_PATTERN = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
DATE_PATTERNS = [
    rf"\b{MONTH_PATTERN}\s+\d{{1,2}}(?:,\s*\d{{4}})?\b",
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
]

DOCUMENT_KEYWORDS = [
    "passport",
    "visa",
    "i-20",
    "ds-2019",
    "bank statement",
    "financial statement",
    "proof of funding",
    "transcript",
    "enrollment verification",
    "housing contract",
    "offer letter",
    "pay stub",
    "tax return",
    "photo id",
]

ACTION_PATTERNS = [
    r"\bplease submit\b",
    r"\bupload\b",
    r"\bcomplete\b",
    r"\bsend\b",
    r"\bfill out\b",
    r"\bsign\b",
    r"\brespond\b",
    r"\bconfirm\b",
    r"\bprovide\b",
]


def _normalize_date(text: str) -> str | None:
    try:
        parsed = parser.parse(text, fuzzy=True)
        return parsed.date().isoformat()
    except Exception:
        return None



def extract_deadlines(text: str) -> list[Deadline]:
    results: list[Deadline] = []
    seen = set()
    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            raw = match.group(0)
            if raw.lower() in seen:
                continue
            seen.add(raw.lower())
            start = max(0, match.start() - 60)
            end = min(len(text), match.end() + 60)
            context = text[start:end].replace("\n", " ").strip()
            results.append(
                Deadline(text=raw, normalized=_normalize_date(raw), context=context)
            )
    return results



def extract_requested_documents(text: str) -> list[RequestedDocument]:
    lowered = text.lower()
    docs: list[RequestedDocument] = []
    for keyword in DOCUMENT_KEYWORDS:
        idx = lowered.find(keyword)
        if idx != -1:
            context = text[max(0, idx - 60): min(len(text), idx + len(keyword) + 60)]
            docs.append(RequestedDocument(name=keyword.title(), context=context.replace("\n", " ")))
    deduped = []
    seen = set()
    for doc in docs:
        if doc.name not in seen:
            seen.add(doc.name)
            deduped.append(doc)
    return deduped



def extract_action_items(text: str) -> list[ActionItem]:
    items: list[ActionItem] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if any(re.search(pattern, lowered) for pattern in ACTION_PATTERNS):
            priority = "high" if "as soon as possible" in lowered or "required" in lowered else "medium"
            items.append(ActionItem(description=stripped, priority=priority, context=stripped))
    return items



def run_extraction(text: str) -> ExtractionResult:
    return ExtractionResult(
        deadlines=extract_deadlines(text),
        documents=extract_requested_documents(text),
        action_items=extract_action_items(text),
    )
