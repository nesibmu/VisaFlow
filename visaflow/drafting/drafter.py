from visaflow.schemas import Plan


def draft_response(plan: Plan) -> str:
    if not plan.tasks:
        return "No action items were identified."

    lines = ["Here is a suggested next-step summary:"]
    for task in plan.tasks:
        lines.append(f"- {task.task} ({task.priority})")

    return "\n".join(lines)
