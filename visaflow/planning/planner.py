from visaflow.schemas import Plan, PlannedTask


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}



def build_plan(extraction) -> Plan:
    tasks: list[PlannedTask] = []

    for deadline in extraction.deadlines:
        tasks.append(
            PlannedTask(
                title=f"Track deadline: {deadline.text}",
                priority="high",
                rationale=f"A deadline was detected in the source text. Normalized date: {deadline.normalized or 'unknown'}."
            )
        )

    for document in extraction.documents:
        tasks.append(
            PlannedTask(
                title=f"Prepare document: {document.name}",
                priority="high",
                rationale="This document appears to be requested in the workflow materials."
            )
        )

    for item in extraction.action_items:
        tasks.append(
            PlannedTask(
                title=item.description,
                priority=item.priority,
                rationale="This sentence was identified as a likely required action."
            )
        )

    tasks.sort(key=lambda task: (PRIORITY_ORDER.get(task.priority, 3), task.title.lower()))
    return Plan(tasks=tasks)
