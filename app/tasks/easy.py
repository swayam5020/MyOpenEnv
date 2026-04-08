from app.models import Email

TASK = {
    "email": Email(
        id="1",
        subject="Refund needed",
        body="I want a refund for my purchase"
    ),
    "expected": {
        "category": "refund",
        "priority": "medium",
        "route": "billing"
    }
}