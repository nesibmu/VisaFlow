from visaflow.schemas import ExtractionResult, Plan



def render_extraction(extraction: ExtractionResult) -> str:
    lines = ["EXTRACTION RESULTS"]

    lines.append("\nDeadlines:")
    if extraction.deadlines:
        for deadline in extraction.deadlines:
            lines.append(f"- {deadline.text} (normalized: {deadline.normalized})")
    else:
        lines.append("- None found")

    lines.append("\nRequested documents:")
    if extraction.documents:
        for document in extraction.documents:
            lines.append(f"- {document.name}")
    else:
        lines.append("- None found")

    lines.append("\nAction items:")
    if extraction.action_items:
        for item in extraction.action_items:
            lines.append(f"- [{item.priority}] {item.description}")
    else:
        lines.append("- None found")

    return "\n".join(lines)



def render_plan(plan: Plan) -> str:
    lines = ["\nPLANNED TASKS"]
    for task in plan.tasks:
        lines.append(f"- [{task.priority}] {task.title}")
        lines.append(f"  reason: {task.rationale}")
    return "\n".join(lines)
