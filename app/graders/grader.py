def grade(task, action, state):
    expected = task["expected"]
    score = 0.0
    feedback = []

    content = action.content.lower()

    # Category
    if expected["category"].lower() in content:
        score += 0.25
    else:
        feedback.append("wrong category")

    # Priority
    if expected["priority"].lower() in content:
        score += 0.20
    else:
        feedback.append("wrong priority")

    # Route
    if expected["route"].lower() in content:
        score += 0.20
    else:
        feedback.append("wrong route")

    # Escalation (important for HARD)
    if expected.get("needs_escalation"):
        if "escalate" in content:
            score += 0.15
        else:
            feedback.append("no escalation")

    # Quality
    if "resolution:" in content:
        score += 0.10

    # Efficiency
    if state["step"] == 1:
        score += 0.10

    score = max(0.0, min(1.0, score))
    return score, ", ".join(feedback)