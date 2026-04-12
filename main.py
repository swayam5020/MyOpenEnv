from fastapi import FastAPI
from pydantic import BaseModel
from app.env import SupportOpsEnv
from app.models import Action

app = FastAPI()
env = SupportOpsEnv()

class StepRequest(BaseModel):
    action_type: str
    content: str

@app.post("/reset")
def reset(task_name: str = "easy"):
    obs = env.reset(task_name)
    return {
        "email": obs.email,
        "conversation": obs.conversation,
        "status": obs.status
    }

@app.post("/step")
def step(req: StepRequest):
    action = Action(
        action_type=req.action_type,
        content=req.content
    )

    obs, reward, done, _ = env.step(action)

    return {
        "observation": {
            "email": obs.email,
            "conversation": obs.conversation,
            "status": obs.status
        },
        "reward": reward.score,
        "done": done,
        "feedback": reward.feedback
    }