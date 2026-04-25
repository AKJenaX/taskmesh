from env.taskmesh_env import TaskMeshEnv
import json
from pathlib import Path

from backend.scheduler.utils import load_learned_weights


EPISODES = 50


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

def _pick_action(tasks, policy, weights, current_time):
    if not tasks:
        return 0

    if policy == "baseline":
        scores = [
            (_get(task, "priority", 0) - 0.5 * _get(task, "duration", 0))
            for task in tasks
        ]
        return scores.index(max(scores))
    else:
        w_priority = weights["w_priority"]
        w_duration = weights["w_duration"]

        def score(task):
            priority = float(_get(task, "priority", 0))
            duration = float(_get(task, "duration", 0))
            return (
                (w_priority * priority * 3.0)
                - (w_duration * duration * 1.5)
                - (0.2 * current_time)
            )

    return int(max(range(len(tasks)), key=lambda i: score(tasks[i])))


def _step_env(env, action):
    step_out = env.step(action)
    if len(step_out) == 5:
        next_state, _reward, terminated, truncated, _info = step_out
        done = bool(terminated or truncated)
    else:
        next_state, _reward, done, _info = step_out
    return next_state, bool(done)


def run_episode(policy, weights, env=None):
    env = env or TaskMeshEnv()
    reset_out = env.reset()
    state = reset_out[0] if isinstance(reset_out, tuple) else reset_out

    done = False
    num_tasks = 0

    while not done:
        tasks = _extract_tasks(state)
        if not tasks:
            break

        action = _pick_action(tasks, policy, weights, env.current_time)
        selected_task = tasks[action]
        duration = int(_get(selected_task, "duration", 0))
        num_tasks += 1

        state, done = _step_env(env, action)

    metrics = {
        "avg_wait_time": (env.total_wait_time / num_tasks) if num_tasks else 0.0,
        "throughput": num_tasks,
        "tail_latency": env.current_time,
    }
    return metrics


def _aggregate(metrics_list):
    if not metrics_list:
        return {"avg_wait_time": 0.0, "throughput": 0.0, "tail_latency": 0.0}

    count = len(metrics_list)
    return {
        "avg_wait_time": sum(m["avg_wait_time"] for m in metrics_list) / count,
        "throughput": sum(m["throughput"] for m in metrics_list) / count,
        "tail_latency": sum(m["tail_latency"] for m in metrics_list) / count,
    }


def _pct_improvement(baseline_value, trained_value):
    if baseline_value == 0:
        return 0.0
    return ((baseline_value - trained_value) / baseline_value) * 100.0


def main():
    weights = load_learned_weights()
    baseline_env = TaskMeshEnv()
    trained_env = TaskMeshEnv()

    baseline_runs = [run_episode("baseline", weights, env=baseline_env) for _ in range(EPISODES)]
    trained_runs = [run_episode("trained", weights, env=trained_env) for _ in range(EPISODES)]

    baseline_metrics = _aggregate(baseline_runs)
    trained_metrics = _aggregate(trained_runs)

    improvement = {
        "avg_wait_time": _pct_improvement(
            baseline_metrics["avg_wait_time"], trained_metrics["avg_wait_time"]
        ),
        "tail_latency": _pct_improvement(
            baseline_metrics["tail_latency"], trained_metrics["tail_latency"]
        ),
    }

    print("Baseline:")
    print(f"  avg_wait_time: {baseline_metrics['avg_wait_time']:.2f}")
    print(f"  tail_latency: {baseline_metrics['tail_latency']:.2f}")
    print()
    print("Trained:")
    print(f"  avg_wait_time: {trained_metrics['avg_wait_time']:.2f}")
    print(f"  tail_latency: {trained_metrics['tail_latency']:.2f}")
    print()
    print("Improvement:")
    print(f"  avg_wait_time: {improvement['avg_wait_time']:.2f}%")
    print(f"  tail_latency: {improvement['tail_latency']:.2f}%")

    output = {
        "baseline": baseline_metrics,
        "trained": trained_metrics,
        "improvement": improvement,
    }
    output_path = Path(__file__).resolve().parent / "benchmark_results.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nSaved benchmark results to: {output_path}")


if __name__ == "__main__":
    main()
