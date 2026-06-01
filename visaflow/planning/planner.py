from visaflow.schemas import Plan, PlannedTask


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SOURCE_ORDER = {"deadline": 0, "requested_document": 1, "action_item": 2}


def infer_priority(task_text: str, source: str) -> str:
    lowered = task_text.lower()

    if source == "deadline":
        return "high"

    if source == "requested_document":
        if any(word in lowered for word in ["passport", "bank statement", "i-20", "agreement", "enrollment"]):
            return "high"
        return "medium"

    if source == "action_item":
        if any(word in lowered for word in ["as soon as possible", "respond", "reply", "confirm"]):
            return "medium"
        if any(word in lowered for word in ["submit", "upload"]):
            return "high"
        return "low"

    return "medium"


def deduplicate_tasks(tasks):
    seen = set()
    unique_tasks = []

    for task in tasks:
        key = (task.task.lower(), task.source)
        if key not in seen:
            seen.add(key)
            unique_tasks.append(task)

    return unique_tasks


def sort_tasks(tasks):
    return sorted(
        tasks,
        key=lambda task: (
            PRIORITY_ORDER.get(task.priority, 99),
            SOURCE_ORDER.get(task.source, 99),
            task.task.lower(),
        ),
    )


def build_task_plan(extracted: dict) -> Plan:
    tasks = []

    for deadline in extracted.get("deadlines", []):
        task_text = f"Track deadline: {deadline}"
        tasks.append(
            PlannedTask(
                task=task_text,
                priority=infer_priority(task_text, "deadline"),
                source="deadline",
            )
        )

    for document in extracted.get("requested_documents", []):
        task_text = f"Prepare document: {document}"
        tasks.append(
            PlannedTask(
                task=task_text,
                priority=infer_priority(task_text, "requested_document"),
                source="requested_document",
            )
        )

    for action in extracted.get("action_items", []):
        task_text = f"Complete action: {action}"
        tasks.append(
            PlannedTask(
                task=task_text,
                priority=infer_priority(action, "action_item"),
                source="action_item",
            )
        )

    tasks = deduplicate_tasks(tasks)
    tasks = sort_tasks(tasks)

    return Plan(tasks=tasks)
