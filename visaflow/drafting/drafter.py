from visaflow.schemas import Plan



def draft_reply(plan: Plan) -> str:
    high_priority = [task.title for task in plan.tasks if task.priority == "high"]
    selected = high_priority[:3] if high_priority else [task.title for task in plan.tasks[:3]]

    body_lines = [
        "Hello,",
        "",
        "Thank you for the update. I reviewed the requested items and I am currently working through the next steps.",
    ]

    if selected:
        body_lines.append("")
        body_lines.append("From my understanding, the main items I need to complete are:")
        for item in selected:
            body_lines.append(f"- {item}")

    body_lines.extend([
        "",
        "Please let me know if there is anything else I should submit or prioritize.",
        "",
        "Best,",
        "Nesib",
    ])
    return "\n".join(body_lines)



def draft_summary(plan: Plan) -> str:
    if not plan.tasks:
        return "No clear action items were identified yet."

    lines = ["Next-step summary:"]
    for task in plan.tasks[:5]:
        lines.append(f"- [{task.priority}] {task.title}")
    return "\n".join(lines)
