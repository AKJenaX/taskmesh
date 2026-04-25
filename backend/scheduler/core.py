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


def _compute_metrics(schedule):
    if not schedule:
        return {
            "avg_wait_time": 0,
            "throughput": 0,
            "tail_latency": 0
        }

    wait_times = [task["start"] for task in schedule]

    avg_wait_time = sum(wait_times) / len(wait_times)
    throughput = len(schedule)
    tail_latency = max(wait_times) if wait_times else 0

    return {
        "avg_wait_time": avg_wait_time,
        "throughput": throughput,
        "tail_latency": tail_latency
    }


def _process_schedule(ordered_tasks):
    schedule = []
    current_time = 0

    for task in ordered_tasks:
        start = current_time
        end = start + task.get("duration", 0)
        schedule.append({
            "task_id": task["id"],
            "start": start,
            "end": end,
            "score": 0.0
        })
        current_time = end

    metrics = _compute_metrics(schedule)

    return {
        "schedule": schedule,
        "metrics": metrics
    }


def baseline_scheduler(tasks):
    ordered_tasks = sorted(tasks, key=lambda x: x.get("priority", 1), reverse=True)
    return _process_schedule(ordered_tasks)


def rl_scheduler(tasks, weights=None):
    if weights is None:
        weights = load_learned_weights()

    remaining = [dict(t) for t in tasks]
    ordered_tasks = []

    if not remaining:
        return _process_schedule([])

    while remaining:
        best_idx = max(
            range(len(remaining)),
            key=lambda i: (
                weights["w_priority"] * (remaining[i].get("priority", 0) / 5.0)
                + weights["w_deadline"] * (1 / (remaining[i].get("deadline", 0) + 1.0))
                - weights["w_duration"] * (remaining[i].get("duration", 0) / 10.0)
            )
        )
        ordered_tasks.append(remaining.pop(best_idx))

    return _process_schedule(ordered_tasks)


def run_scheduler(request, algorithm="baseline"):
    tasks = request.get("tasks", [])

    if not tasks:
        return {
            "schedule": [],
            "metrics": {
                "avg_wait_time": 0,
                "throughput": 0,
                "tail_latency": 0
            }
        }

    if algorithm == "baseline":
        result = baseline_scheduler(tasks)
    elif algorithm == "rl":
        result = rl_scheduler(tasks)
    else:
        result = {
            "schedule": [],
            "metrics": {
                "avg_wait_time": 0,
                "throughput": 0,
                "tail_latency": 0
            }
        }
        
    return result
