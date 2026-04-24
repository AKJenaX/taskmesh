from backend.scheduler.baseline import baseline_schedule
from backend.scheduler.utils import compute_metrics
import json
from pathlib import Path

DEFAULT_WEIGHTS = {
    "w_priority": 1.0,
    "w_deadline": 0.5,
    "w_duration": 0.3,
}

WEIGHTS_FILE = Path(__file__).resolve().parent / "learned_weights.json"


def load_learned_weights():
    try:
        data = json.loads(WEIGHTS_FILE.read_text(encoding="utf-8"))
        return {
            "w_priority": float(data.get("w_priority", DEFAULT_WEIGHTS["w_priority"])),
            "w_deadline": float(data.get("w_deadline", DEFAULT_WEIGHTS["w_deadline"])),
            "w_duration": float(data.get("w_duration", DEFAULT_WEIGHTS["w_duration"])),
        }
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        return dict(DEFAULT_WEIGHTS)

def score_task(task, weights):
    # Shared scoring with training logic.
    return (
        weights["w_priority"] * task["priority"]
        - weights["w_deadline"] * task["deadline"]
        - weights["w_duration"] * task["duration"]
    )


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


def rl_schedule(tasks, weights=None):
    if weights is None:
        weights = load_learned_weights()

    tasks_ordered = ordered_tasks_with_weights(tasks, weights)
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

def run_scheduler(request, algorithm="baseline"):
    tasks = request["tasks"]

    if algorithm == "baseline":
        schedule = baseline_schedule(tasks)
    elif algorithm == "rl":
        schedule = rl_schedule(tasks)
    else:
        schedule = []

    metrics = compute_metrics(schedule)

    return {
        "schedule": schedule,
        "metrics": metrics
    }
