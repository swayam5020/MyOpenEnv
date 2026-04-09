import os, json, re
from typing import List, Optional
from openai import OpenAI

from app.env import SupportOpsEnv
from app.models import Action

# ================= CONFIG =================
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

TASK_NAME = os.getenv("TASK_NAME", "easy")
BENCHMARK = "SupportOpsEnv"

MAX_STEPS = 1

# ================= LOGGER =================
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ================= SAFE JSON =================
def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Invalid JSON")


# ================= MODEL =================
def get_model_response(client: OpenAI, obs) -> dict:
    prompt = f"""
You are an AI support agent.

STRICT RULES:
- Output ONLY JSON
- No explanations
- No markdown

FORMAT:
{{
  "action_type": "reply",
  "content": "category: <value>, priority: <value>, route: <value>, resolution: <short text>"
}}

Allowed:
category: billing / technical
priority: low / medium / high
route: finance / tech / support

Email:
{obs.email.body}

Conversation:
{obs.conversation}
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = completion.choices[0].message.content.strip()
    return extract_json(raw)


# ================= MAIN =================
def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = SupportOpsEnv()

    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs = env.reset(task_name=TASK_NAME)

        for step in range(1, MAX_STEPS + 1):

            action_json = get_model_response(client, obs)

            action = Action(**action_json)

            obs, reward_obj, done, _ = env.step(action)

            reward = reward_obj.score if reward_obj else 0.0
            rewards.append(reward)

            steps_taken = step

            log_step(
                step=step,
                action=str(action_json),
                reward=reward,
                done=done,
                error=None,
            )

            if done:
                break

        score = sum(rewards) / len(rewards) if rewards else 0.0
        success = score >= 0.5

    except Exception as e:
        log_step(steps_taken, "error", 0.0, True, str(e))
        success = False
        score = 0.0

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    main()