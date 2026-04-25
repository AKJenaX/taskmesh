import random
import json
from pathlib import Path
import matplotlib.pyplot as plt

from backend.scheduler.utils import compute_metrics
from backend.scheduler.baseline import baseline_schedule

DEFAULT_WEIGHTS = {
    "w_priority": 1.0,
    "w_deadline": 0.5,
    "w_duration": 0.3,
}

BEST_WEIGHTS = dict(DEFAULT_WEIGHTS)
BEST_REWARD = float("-inf")
SEED = 42
WEIGHTS_FILE = Path(__file__).resolve().parents[1] / "backend" / "scheduler" / "learned_weights.json"

def random_task():
    return {
        "id": str(random.randint(1, 10000)),
        "title": "Task",
        "priority": random.randint(1, 5),
        "deadline": random.randint(5, 50),
        "duration": random.randint(1, 10)
    }

def score_task(task, weights):
    return (
        weights["w_priority"] * (task["priority"] / 5.0)
        + weights["w_deadline"] * (1 / (task["deadline"] + 1.0))
        - weights["w_duration"] * (task["duration"] / 10.0)
    )

def ordered_tasks_with_weights(tasks, weights):
    remaining = [dict(t) for t in tasks]
    ordered = []
    
    if not remaining:
        return []

    while remaining:
        best_idx = max(
            range(len(remaining)),
            key=lambda i: score_task(remaining[i], weights)
        )
        ordered.append(remaining.pop(best_idx))

    return ordered

def execute_environment(tasks_ordered):
    schedule = []
    current_time = 0
    for task in tasks_ordered:
        start = current_time
        end = start + task["duration"]
        schedule.append({
            "task_id": task["id"],
            "start": start,
            "end": end,
            "score": 0.0
        })
        current_time = end
    return schedule

def compute_local_metrics(schedule):
    if not schedule:
        return {"avg_wait_time": 0, "throughput": 0, "tail_latency": 0}
    wait_times = [task["start"] for task in schedule]
    return {
        "avg_wait_time": sum(wait_times) / len(wait_times),
        "throughput": len(schedule),
        "tail_latency": max(wait_times)
    }

def compute_reward(rl_metrics):
    return (
        10
        - rl_metrics["avg_wait_time"] * 0.6
        - rl_metrics["tail_latency"] * 0.4
    )

def evaluate_weights(tasks, weights):
    action_order = ordered_tasks_with_weights(tasks, weights)
    rl_schedule = execute_environment(action_order)
    rl_metrics = compute_local_metrics(rl_schedule)
    reward = compute_reward(rl_metrics)
    return reward, rl_metrics

def main():
    random.seed(SEED)
    
    try:
        if WEIGHTS_FILE.exists():
            data = json.loads(WEIGHTS_FILE.read_text(encoding="utf-8"))
            prev_weights = {
                "w_priority": float(data.get("w_priority", DEFAULT_WEIGHTS["w_priority"])),
                "w_deadline": float(data.get("w_deadline", DEFAULT_WEIGHTS["w_deadline"])),
                "w_duration": float(data.get("w_duration", DEFAULT_WEIGHTS["w_duration"])),
            }
        else:
            prev_weights = dict(DEFAULT_WEIGHTS)
    except Exception:
        prev_weights = dict(DEFAULT_WEIGHTS)
        
    # Generate a fixed validation set for stable comparison
    val_tasks = [random_task() for _ in range(50)]
    
    prev_best_reward, _ = evaluate_weights(val_tasks, prev_weights)
    
    episodes = 300
    rewards = []
    
    best_reward = float("-inf")
    best_weights = dict(prev_weights)
    
    print(f"Initial Baseline Reward (from existing weights): {prev_best_reward:.2f}")
    print("Episode\tReward\tBestReward")
    
    for ep in range(1, episodes + 1):
        weights = {
            "w_priority": random.uniform(0.5, 3.0),
            "w_deadline": random.uniform(0.1, 2.0),
            "w_duration": random.uniform(0.1, 2.0),
        }

        # Evaluate on the fixed validation tasks so comparison is fair
        total_reward, _ = evaluate_weights(val_tasks, weights)
        rewards.append(total_reward)

        if total_reward > best_reward:
            best_reward = total_reward
            best_weights = weights.copy()

        if ep % 20 == 0:
            print(f"Episode {ep} -> reward {total_reward:.2f}, best tracking {best_reward:.2f}")

    print("\nTraining complete")
    if best_reward > prev_best_reward:
        print(f"New best reward found: {best_reward:.2f} (Previous: {prev_best_reward:.2f})")
        final_weights = best_weights
    else:
        print(f"Keeping previous best weights (Previous: {prev_best_reward:.2f} >= New: {best_reward:.2f})")
        final_weights = prev_weights

    WEIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    WEIGHTS_FILE.write_text(json.dumps(final_weights, indent=2), encoding="utf-8")
    print(f"\nFinal weights: {final_weights}")
    print(f"Saved learned weights to: {WEIGHTS_FILE}")
    
    with open("scripts/rewards.json", "w") as f:
        json.dump(rewards, f)

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_path = output_dir / "reward_plot.png"

    plt.figure()
    plt.plot(range(1, episodes + 1), rewards)
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.title("Training Reward Curve")
    plt.savefig(plot_path)
    plt.close()
    print("Reward plot saved to outputs/reward_plot.png")

if __name__ == "__main__":
    main()

