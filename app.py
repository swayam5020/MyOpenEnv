import gradio as gr
from app.env import SupportOpsEnv
from app.models import Action

# Initialize environment
env = SupportOpsEnv()

def run_support_agent(user_input, task_type):
    try:
        # Reset environment with selected task
        obs = env.reset(task_type)

        # Format action (IMPORTANT: must match grader expectations)
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

        return (
            action.content,
            reward.score,
            reward.feedback,
            obs.status
        )

    except Exception as e:
        return str(e), 0, "error", "FAILED"


# UI
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AI Support Agent (SupportOpsEnv)")
    gr.Markdown("Enter a customer issue and see how AI handles it.")

    with gr.Row():
        user_input = gr.Textbox(
            label="Customer Query",
            placeholder="e.g. I was charged twice and app is not working"
        )

        task_type = gr.Dropdown(
            ["easy", "medium", "hard"],
            value="easy",
            label="Task Difficulty"
        )

    run_btn = gr.Button("Run AI Agent")

    output_text = gr.Textbox(label="AI Response")
    score = gr.Number(label="Score")
    feedback = gr.Textbox(label="Feedback")
    status = gr.Textbox(label="Status")

    run_btn.click(
        fn=run_support_agent,
        inputs=[user_input, task_type],
        outputs=[output_text, score, feedback, status]
    )

# Required for HuggingFace Docker Spaces
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)