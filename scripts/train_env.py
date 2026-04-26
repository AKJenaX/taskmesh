from env.taskmesh_env import TaskMeshEnv
import json
import random
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import PPOTrainer, PPOConfig


EPISODES = 200
STEP_SIZE = 0.01


def _get(item, key, default=0):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _extract_tasks(state):
    if isinstance(state, dict) and "tasks" in state:
        return state["tasks"]
    if isinstance(state, list):
        return state
    if hasattr(state, "tasks"):
        return getattr(state, "tasks")
    return []


def _score_task(task, w_priority, w_duration, current_time):
    priority = float(_get(task, "priority", 0))
    duration = float(_get(task, "duration", 0))
    return (
        (w_priority * priority)
        - (w_duration * duration)
        - 0.5 * (current_time + duration)
    )


def _pick_action(tasks, w_priority, w_duration, current_time):
    if not tasks:
        return 0
    best_idx = max(
        range(len(tasks)),
        key=lambda i: _score_task(tasks[i], w_priority, w_duration, current_time),
    )
    return int(best_idx)


def _step_env(env, action):
    step_out = env.step(action)
    if len(step_out) == 5:
        next_state, reward, terminated, truncated, _info = step_out
        done = bool(terminated or truncated)
    else:
        next_state, reward, done, _info = step_out
    return next_state, float(reward), bool(done)

def state_to_text(state, current_time):
    tasks = state if isinstance(state, list) else state.get("remaining_tasks", [])
    
    lines = [
        f"Time: {current_time}",
        "",
        "Tasks:"
    ]
    
    for i, task in enumerate(tasks):
        priority = task.get("priority", 0)
        duration = task.get("duration", 0)
        lines.append(f"{i}: priority={priority}, duration={duration}")
        
    lines.append("")
    lines.append("Which task should be executed next? Return only the task index.")
    
    return "\n".join(lines)
def model_predict(state_text, num_tasks):
    inputs = tokenizer(state_text, return_tensors="pt")
    input_ids = inputs["input_ids"]
    
    with torch.no_grad():
        outputs = model.generate(input_ids, max_new_tokens=10, pad_token_id=tokenizer.eos_token_id)
        
    response_ids = outputs[0][input_ids.shape[-1]:]
    output_text = tokenizer.decode(response_ids, skip_special_tokens=True).strip()
    
    try:
        import re
        numbers = re.findall(r'\d+', output_text)
        action = int(numbers[0]) if numbers else 0
    except Exception:
        action = 0
        
    action = max(0, min(action, num_tasks - 1))
    return action, input_ids[0], response_ids

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

config = PPOConfig(
    learning_rate=1e-5,
    batch_size=1,
    mini_batch_size=1
)
ppo_trainer = PPOTrainer(config, model, tokenizer)


def main():
    env = TaskMeshEnv()

    w_priority = random.uniform(0.5, 2.0)
    w_duration = random.uniform(0.5, 2.0)
    best_reward = float("-inf")
    best_weights = {
        "w_priority": w_priority,
        "w_duration": w_duration,
    }

    rewards = []
    weights_history = []

    for ep in range(1, EPISODES + 1):
        reset_out = env.reset()
        state = reset_out[0] if isinstance(reset_out, tuple) else reset_out

        done = False
        total_reward = 0.0

        while not done:
            tasks = _extract_tasks(state)
            state_text = state_to_text(state, env.current_time)
            action, input_ids, response_ids = model_predict(state_text, len(tasks))
            state, reward, done = _step_env(env, action)
            total_reward += reward
            
            reward_tensor = torch.tensor([float(reward)])
            ppo_trainer.step([input_ids], [response_ids], [reward_tensor])

        if total_reward > best_reward:
            best_reward = total_reward
            best_weights = {
                "w_priority": w_priority,
                "w_duration": w_duration,
            }
            w_priority += 0.03
            w_duration -= 0.02
        else:
            w_priority -= 0.01
            w_duration += 0.03

        w_priority += random.uniform(-0.01, 0.01)
        w_duration += random.uniform(-0.01, 0.01)

        w_priority = max(0.1, w_priority)
        w_duration = max(0.1, w_duration)

        rewards.append(total_reward)
        weights_history.append(
            {
                "episode": ep,
                "w_priority": w_priority,
                "w_duration": w_duration,
                "reward": total_reward,
            }
        )

        if ep % 20 == 0:
            print(f"Episode {ep} -> reward {total_reward:.2f}")

    root = Path(__file__).resolve().parents[1]
    scripts_dir = Path(__file__).resolve().parent
    rewards_path = scripts_dir / "rewards.json"
    weights_path = root / "backend" / "scheduler" / "learned_weights.json"

    rewards_path.write_text(json.dumps(rewards, indent=2), encoding="utf-8")
    print(f"Saving weights to: {weights_path}")
    weights_path.write_text(
        json.dumps(
            {
                "w_priority": best_weights["w_priority"],
                "w_duration": best_weights["w_duration"],
                "best_reward": best_reward,
                "weights_history": weights_history,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved rewards to: {rewards_path}")
    print(f"Saved learned weights to: {weights_path}")


if __name__ == "__main__":
    main()
