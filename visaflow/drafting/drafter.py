from visaflow.schemas import Plan


def generate_next_step_summary(plan: Plan) -> str:
    if not plan.tasks:
        return "No immediate action items were identified."

    high_priority = [task for task in plan.tasks if task.priority == "high"]
    medium_priority = [task for task in plan.tasks if task.priority == "medium"]

    lines = ["Next-step summary:"]

    if high_priority:
        lines.append("Handle these first:")
        for task in high_priority[:5]:
            lines.append(f"- {task.task}")

    if medium_priority:
        lines.append("")
        lines.append("Then follow up on:")
        for task in medium_priority[:5]:
            lines.append(f"- {task.task}")

    return "\n".join(lines)


def draft_response(plan: Plan) -> str:
    if not plan.tasks:
        return "No immediate action items were identified."

    high_priority = [task for task in plan.tasks if task.priority == "high"]
    medium_priority = [task for task in plan.tasks if task.priority == "medium"]
    low_priority = [task for task in plan.tasks if task.priority == "low"]

    lines = []
    lines.append("Suggested next steps")
    lines.append("")

    if high_priority:
        lines.append("Urgent:")
        for task in high_priority:
            lines.append(f"- {task.task}")
        lines.append("")

    if medium_priority:
        lines.append("Important follow-up:")
        for task in medium_priority:
            lines.append(f"- {task.task}")
        lines.append("")

    if low_priority:
        lines.append("Lower-priority items:")
        for task in low_priority:
            lines.append(f"- {task.task}")
        lines.append("")

    lines.append("Draft reply:")
    lines.append("Hello,")
    lines.append("")
    lines.append("Thank you for the update. I will work on the requested items and follow up once everything has been submitted.")
    lines.append("")
    lines.append("Best,")
    lines.append("Nesib")

    return "\n".join(lines)


def draft_response_enhanced(plan: Plan) -> str:
    if not plan.tasks:
        return "Hello,\n\nThank you for the message. I do not see any immediate action items right now, but I will review everything again and follow up if needed.\n\nBest,\nNesib"

    high_priority = [task.task for task in plan.tasks if task.priority == "high"]
    medium_priority = [task.task for task in plan.tasks if task.priority == "medium"]

    lines = []
    lines.append("Hello,")
    lines.append("")
    lines.append("Thank you for the update. I have reviewed the requested items and will take care of the next steps.")

    if high_priority:
        lines.append("")
        lines.append("I will prioritize the following first:")
        for task in high_priority[:4]:
            lines.append(f"- {task}")

    if medium_priority:
        lines.append("")
        lines.append("After that, I will follow up on:")
        for task in medium_priority[:3]:
            lines.append(f"- {task}")

    lines.append("")
    lines.append("I will follow up once everything has been submitted or if I need any clarification.")
    lines.append("")
    lines.append("Best,")
    lines.append("Nesib")

    return "\n".join(lines)


def draft_response_with_mode(plan: Plan, enhanced: bool = False) -> str:
    if enhanced:
        return draft_response_enhanced(plan)
    return draft_response(plan)
