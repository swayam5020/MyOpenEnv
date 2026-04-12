import os
from openai import OpenAI
from fastapi import FastAPI
from app.env import SupportOpsEnv
from app.models import Action

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

app = FastAPI()
env = SupportOpsEnv()

@app.get("/")
def home():
    return {"message": "Server is running 🚀"}

@app.post("/run")
def run_agent(user_input: str = "test", task_type: str = "easy"):
    obs = env.reset(task_type)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a support agent.\n\nSTRICT RULES:\n- Output EXACTLY 4 lines\n- No extra text\n- No explanations\n- Format EXACTLY:\n\ncategory: <value>\npriority: <value>\nroute: <value>\nresolution: <value>"},
            {"role": "user", "content": user_input}
        ]
    )

    action_text = response.choices[0].message.content.strip()

    # fallback if format breaks
    if "category:" not in action_text or "priority:" not in action_text:
        action_text = f"""category: billing
priority: medium
route: finance
resolution: {user_input}"""

    action = Action(
        action_type="reply",
        content=action_text
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
if __name__ == "__main__":
    main()