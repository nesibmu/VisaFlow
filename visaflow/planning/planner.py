from visaflow.schemas import Plan, PlannedTask


def build_task_plan(extracted: dict) -> Plan:
    tasks = []

    for deadline in extracted.get("deadlines", []):
        tasks.append(
            PlannedTask(
                task=f"Track deadline: {deadline}",
                priority="high",
                source="deadline",
            )
        )

    for document in extracted.get("requested_documents", []):
        tasks.append(
            PlannedTask(
                task=f"Prepare document: {document}",
                priority="high",
                source="requested_document",
            )
        )

    for action in extracted.get("action_items", []):
        tasks.append(
            PlannedTask(
                task=f"Complete action: {action}",
                priority="medium",
                source="action_item",
            )
        )

    return Plan(tasks=tasks)
