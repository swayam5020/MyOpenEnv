from app.models import Email

TASK = {
    "email": Email(
        id="3",
        subject="Multiple issues",
        body="Charged twice and app not working. no response from support"
    ),
    "expected": {
        "category": "multi",
        "priority": "high",
        "route": "support_lead",
        "needs_escalation": True
    }
}