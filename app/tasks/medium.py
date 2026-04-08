from app.models import Email

TASK = {
    "email": Email(
        id="2",
        subject="App crash urgent",
        body="My app crashes immediately. urgent fix needed"
    ),
    "expected": {
        "category": "technical",
        "priority": "high",
        "route": "engineering"
    }
}