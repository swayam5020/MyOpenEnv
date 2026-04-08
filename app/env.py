from app.models import Observation, Action, Reward
from app.state import init_state
from app.tasks.loader import TASKS
from app.graders.grader import grade


class SupportOpsEnv:
    def __init__(self):
        self.state_data = None
        self.task = None

    def reset(self, task_name="easy"):
        self.task = TASKS[task_name]
        self.state_data = init_state()

        return Observation(
            email=self.task["email"],
            conversation=[],
            status="NEW"
        )

    def step(self, action: Action):
        self.state_data["step"] += 1
        self.state_data["conversation"].append(action.content)

        if "category" in action.content.lower():
            self.state_data["category_history"].append(action.content)

        score, feedback = grade(self.task, action, self.state_data)

        # ✅ CLEAN DONE LOGIC
        done = self.state_data["step"] >= 1

        reward = Reward(score=score, feedback=feedback)

        obs = Observation(
            email=self.task["email"],
            conversation=self.state_data["conversation"],
            status="DONE" if done else "IN_PROGRESS"
        )

        return obs, reward, done, {}

    def state(self):
        return self.state_data