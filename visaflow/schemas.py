from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Deadline:
    text: str
    normalized: Optional[str] = None
    context: Optional[str] = None


@dataclass
class RequestedDocument:
    name: str
    context: Optional[str] = None


@dataclass
class ActionItem:
    description: str
    priority: str = "medium"
    context: Optional[str] = None


@dataclass
class ExtractionResult:
    deadlines: List[Deadline] = field(default_factory=list)
    documents: List[RequestedDocument] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)


@dataclass
class PlannedTask:
    title: str
    priority: str
    rationale: str


@dataclass
class Plan:
    tasks: List[PlannedTask] = field(default_factory=list)
