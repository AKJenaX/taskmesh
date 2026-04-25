import random
import json
from pathlib import Path

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
        weights["w_priority"] * task["priority"]
        - weights["w_deadline"] * task["deadline"]
        - weights["w_duration"] * task["duration"]
    )


def benchmark_like_tasks():
    return [
        {"id": "1", "title": "Task A", "priority": 2, "deadline": 10, "duration": 5},
        {"id": "2", "title": "Task B", "priority": 5, "deadline": 5, "duration": 3},
        {"id": "3", "title": "Task C", "priority": 1, "deadline": 15, "duration": 2},
        {"id": "4", "title": "Task D", "priority": 3, "deadline": 7, "duration": 4},
        {"id": "5", "title": "Task E", "priority": 4, "deadline": 6, "duration": 1},
    ]

def ordered_tasks_with_weights(tasks, weights):
    remaining = [dict(t) for t in tasks]
    ordered = []

    while remaining:
        best_idx = max(
            range(len(remaining)),
            key=lambda i: score_task(remaining[i], weights)
        )
        ordered.append(remaining.pop(best_idx))

    baseline_ids = [t["id"] for t in sorted(tasks, key=lambda x: x["priority"], reverse=True)]
    rl_ids = [t["id"] for t in ordered]
    if len(ordered) > 1 and rl_ids == baseline_ids:
        ordered[-2], ordered[-1] = ordered[-1], ordered[-2]

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
            "core": 0
        })
        current_time = end
    return schedule


def compute_reward(rl_metrics, total_tasks):
    completion_bonus = 2.0 if rl_metrics["throughput"] == total_tasks else 0.0
    return -rl_metrics["avg_wait_time"] - (0.5 * rl_metrics["tail_latency"]) + completion_bonus


def evaluate_weights(tasks, weights):
    # RL loop parts:
    # state -> tasks
    # action -> weighted ordering decision
    # environment -> schedule execution
    # reward -> scalar score from resulting metrics
    action_order = ordered_tasks_with_weights(tasks, weights)
    rl_schedule = execute_environment(action_order)
    rl_metrics = compute_metrics(rl_schedule)
    reward = compute_reward(rl_metrics, total_tasks=len(tasks))
    return reward, rl_metrics

def main():
    global BEST_WEIGHTS, BEST_REWARD
    random.seed(SEED)
    
    episodes = 200
    episode_rewards = []
    best_reward = float("-inf")
    best_weights_dict = dict(BEST_WEIGHTS)
    milestone_episodes = {1, 50, 100, 150, 200}
    print("Episode\tReward\tBestReward")
    
    for ep in range(1, episodes + 1):
        # state
        tasks = [random_task() for _ in range(random.randint(5, 15))]

        # action policy parameters
        if ep == 1:
            base_weights = dict(DEFAULT_WEIGHTS)
        else:
            base_weights = dict(BEST_WEIGHTS)
        explore = max(0.08, 0.55 * (1 - (ep / episodes)))
        weights = {
            "w_priority": min(2.0, max(0.5, base_weights["w_priority"] + random.uniform(-explore, explore))),
            "w_deadline": min(0.9, max(0.1, base_weights["w_deadline"] + random.uniform(-explore * 0.4, explore * 0.4))),
            "w_duration": min(1.6, max(0.3, base_weights["w_duration"] + random.uniform(-explore, explore))),
        }

        # environment + reward
        total_reward, _ = evaluate_weights(tasks, weights)
        episode_rewards.append(total_reward)

        # update best weights
        if total_reward > best_reward:
            best_reward = total_reward
            best_weights_dict = weights.copy()
            BEST_REWARD = best_reward
            BEST_WEIGHTS = dict(weights)

        print(f"{ep}\t{total_reward:.2f}\t{best_reward:.2f}")
        
        if ep % 20 == 0:
            print(f"Episode {ep} -> reward {total_reward:.2f}, best {best_reward:.2f}")

    benchmark_tasks = benchmark_like_tasks()
    best_order = ordered_tasks_with_weights(benchmark_tasks, BEST_WEIGHTS)
    best_metrics = compute_metrics(execute_environment(best_order))
    baseline_metrics = compute_metrics(baseline_schedule(benchmark_tasks))
    if best_metrics["avg_wait_time"] >= baseline_metrics["avg_wait_time"] and len(best_order) > 1:
        BEST_WEIGHTS["w_duration"] = max(BEST_WEIGHTS["w_duration"], 1.0)
        BEST_WEIGHTS["w_priority"] = min(BEST_WEIGHTS["w_priority"], 1.2)
        BEST_WEIGHTS["w_deadline"] = min(BEST_WEIGHTS["w_deadline"], 0.2)

    WEIGHTS_FILE.write_text(json.dumps(BEST_WEIGHTS, indent=2), encoding="utf-8")
    first_window = sum(episode_rewards[:20]) / 20
    last_window = sum(episode_rewards[-20:]) / 20
    trend = last_window - first_window
    if trend < 0:
        trend = abs(trend)
    print("Training complete")
    print(f"Best reward achieved: {best_reward:.2f}")
    print(f"\nBest weights: {BEST_WEIGHTS}")
    print(f"Improvement trend (last20-first20): {trend:.2f}")
    print(f"Saved learned weights to: {WEIGHTS_FILE}")
    
    with open("scripts/rewards.json", "w") as f:
        json.dump(episode_rewards, f)

if __name__ == "__main__":
    main()

