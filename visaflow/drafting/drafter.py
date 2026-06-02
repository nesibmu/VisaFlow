from visaflow.schemas import Plan


def generate_next_step_summary(plan: Plan) -> str:
    if not plan.tasks:
        return "No immediate action items were identified."

    urgent = [task for task in plan.tasks if task.status == "urgent"]
    ready = [task for task in plan.tasks if task.status == "ready"]
    blocked = [task for task in plan.tasks if task.status == "blocked"]

    lines = ["Next-step summary:"]

    if urgent:
        lines.append("Handle these first:")
        for task in urgent[:5]:
            lines.append(f"- {task.task}")

    if ready:
        lines.append("")
        lines.append("Ready to work on:")
        for task in ready[:5]:
            lines.append(f"- {task.task}")

    if blocked:
        lines.append("")
        lines.append("Blocked pending other steps:")
        for task in blocked[:5]:
            lines.append(f"- {task.task}")

    return "\n".join(lines)


def generate_action_checklist(plan: Plan) -> str:
    if not plan.tasks:
        return "No checklist items available."

    lines = ["Action checklist:"]
    for task in plan.tasks:
        prefix = "[ ]"
        lines.append(f"{prefix} {task.task} ({task.status})")

    return "\n".join(lines)


def draft_response(plan: Plan) -> str:
    if not plan.tasks:
        return "No immediate action items were identified."

    urgent = [task for task in plan.tasks if task.status == "urgent"]
    ready = [task for task in plan.tasks if task.status == "ready"]
    blocked = [task for task in plan.tasks if task.status == "blocked"]

    lines = []
    lines.append("Suggested next steps")
    lines.append("")

    if urgent:
        lines.append("Urgent:")
        for task in urgent:
            lines.append(f"- {task.task}")
        lines.append("")

    if ready:
        lines.append("Ready:")
        for task in ready:
            lines.append(f"- {task.task}")
        lines.append("")

    if blocked:
        lines.append("Blocked:")
        for task in blocked:
            lines.append(f"- {task.task}")
        lines.append("")

    lines.append("Draft reply:")
    lines.append("Hello,")
    lines.append("")
    lines.append("Thank you for the update. I will work through the requested items and follow up once everything has been submitted.")
    lines.append("")
    lines.append("Best,")
    lines.append("Nesib")

    return "\n".join(lines)


def draft_response_enhanced(plan: Plan) -> str:
    if not plan.tasks:
        return "Hello,\n\nThank you for the message. I do not see any immediate action items right now, but I will review everything again and follow up if needed.\n\nBest,\nNesib"

    urgent = [task.task for task in plan.tasks if task.status == "urgent"]
    ready = [task.task for task in plan.tasks if task.status == "ready"]
    blocked = [task.task for task in plan.tasks if task.status == "blocked"]

    lines = []
    lines.append("Hello,")
    lines.append("")
    lines.append("Thank you for the update. I reviewed the request and organized the next steps on my side.")

    if urgent:
        lines.append("")
        lines.append("I will prioritize the following first:")
        for task in urgent[:4]:
            lines.append(f"- {task}")

    if ready:
        lines.append("")
        lines.append("I can also move forward on:")
        for task in ready[:4]:
            lines.append(f"- {task}")

    if blocked:
        lines.append("")
        lines.append("A few items depend on earlier steps being completed first:")
        for task in blocked[:3]:
            lines.append(f"- {task}")

    lines.append("")
    lines.append("I will follow up once the requested items have been submitted, or sooner if I need clarification.")
    lines.append("")
    lines.append("Best,")
    lines.append("Nesib")

    return "\n".join(lines)


def draft_response_with_mode(plan: Plan, enhanced: bool = False) -> str:
    if enhanced:
        return draft_response_enhanced(plan)
    return draft_response(plan)
