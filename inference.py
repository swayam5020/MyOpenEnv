import os, json, re
from openai import OpenAI
from app.env import SupportOpsEnv
from app.models import Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

env = SupportOpsEnv()
tasks = ["easy", "medium", "hard"]


# 🔥 SAFE JSON PARSER (CRITICAL FIX)
def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("No valid JSON found")


for task_name in tasks:
    print(f"[START] task={task_name}")

    obs = env.reset(task_name)
    rewards = []
    done = False
    step = 0

    try:
        while not done and step < 3:
            step += 1

            prompt = f"""
You are an AI support agent.

STRICT RULES:
- Output ONLY JSON
- No explanations
- No markdown
- No email format

FORMAT EXACTLY:
{{
  "action_type": "reply",
  "content": "category: <value>, priority: <value>, route: <value>, resolution: <short text>"
}}

Use ONLY these values:
- category: billing / technical
- priority: low / medium / high
- route: finance / tech / support

If complex issue → include word "escalate"

---

Email:
{obs.email.body}

Conversation:
{obs.conversation}
"""

            res = client.chat.completions.create(
                model=MODEL_NAME,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )

            raw_output = res.choices[0].message.content.strip()
            print("MODEL OUTPUT:", raw_output)

            action_json = extract_json(raw_output)
            action = Action(**action_json)

            obs, reward, done, _ = env.step(action)

            rewards.append(reward.score)

            print(f"[STEP] step={step} reward={reward.score:.2f} done={done}")

        score = sum(rewards) / len(rewards) if rewards else 0
        success = score > 0.5

        print(f"[END] success={success} steps={step} score={score:.2f}")

    except Exception as e:
        print("ERROR:", str(e))
        print(f"[END] success=false steps={step} score=0.00")