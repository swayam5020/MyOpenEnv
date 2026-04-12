from fastapi import FastAPI
from app.env import SupportOpsEnv
from app.models import Action

app = FastAPI()
env = SupportOpsEnv()

@app.get("/")
def home():
    return {"message": "Server is running 🚀"}

@app.post("/run")
def run_agent(user_input: str = "test", task_type: str = "easy"):
    obs = env.reset(task_type)

    action_text = f"""
category: billing
priority: high
route: finance
resolution: {user_input}
    """

    action = Action(
        action_type="reply",
        content=action_text.strip()
    )

    obs, reward, done, _ = env.step(action)

    return {
        "response": action.content,
        "score": reward.score,
        "feedback": reward.feedback,
        "status": obs.status
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)