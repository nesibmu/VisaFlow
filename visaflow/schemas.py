from dataclasses import dataclass, field
from typing import List


@dataclass
class Document:
    path: str
    document_type: str
    text: str
    sections: List[str] = field(default_factory=list)
