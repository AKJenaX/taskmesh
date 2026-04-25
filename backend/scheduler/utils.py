import json
from pathlib import Path


def load_learned_weights():
    root = Path(__file__).resolve().parents[2]
    weights_path = root / "backend" / "scheduler" / "learned_weights.json"

    try:
        data = json.loads(weights_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        data = {}

    return {
        "w_priority": float(data.get("w_priority", 1.0)),
        "w_duration": float(data.get("w_duration", 1.0)),
    }


def compute_metrics(schedule):
    if not schedule:
        return {
            "avg_wait_time": 0,
            "throughput": 0,
            "tail_latency": 0
        }

    wait_times = [task["start"] for task in schedule]

    avg_wait_time = sum(wait_times) / len(wait_times)
    throughput = len(schedule)
    tail_latency = max(wait_times)

    return {
        "avg_wait_time": avg_wait_time,
        "throughput": throughput,
        "tail_latency": tail_latency
    }
