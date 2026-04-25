import json
import math
import random
from pathlib import Path

from backend.scheduler.utils import load_learned_weights


DEFAULT_WEIGHTS = {
    "w_priority": 1.0,
    "w_deadline": 0.5,
    "w_duration": 0.3,
}

def _to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def _get(task, key, default=0):
    if isinstance(task, dict):
        return task.get(key, default)
    return getattr(task, key, default)


def _normalize_tasks(tasks):
    normalized = []
    for idx, task in enumerate(tasks):
        task_id = _to_int(_get(task, "id", default=idx + 1), default=idx + 1)
        duration = max(0, _to_int(_get(task, "duration", default=0), default=0))
        priority = _to_int(_get(task, "priority", default=0), default=0)
        deadline = _to_int(_get(task, "deadline", default=0), default=0)
        normalized.append(
            {
                "id": task_id,
                "duration": duration,
                "priority": priority,
                "deadline": deadline,
            }
        )
    return normalized


def _score_task(task, weights):
    return (
        weights["w_priority"] * task["priority"]
        - weights["w_deadline"] * task["deadline"]
        - weights["w_duration"] * task["duration"]
    )


def _build_schedule(tasks_ordered):
    schedule = []
    current_time = 0

    for task in tasks_ordered:
        start = int(current_time)
        end = int(start + task["duration"])
        schedule.append(
            {
                "task_id": int(task["id"]),
                "start": int(start),
                "end": int(end),
                "score": 0.0,
            }
        )
        current_time = end

    return schedule


def _compute_metrics(schedule):
    if not schedule:
        return {
            "avg_wait_time": 0,
            "throughput": 0,
            "tail_latency": 0,
        }

    wait_times = [int(item["start"]) for item in schedule]
    completion_times = [int(item["end"]) for item in schedule]

    return {
        "avg_wait_time": int(sum(wait_times) / len(wait_times)),
        "throughput": int(len(schedule)),
        "tail_latency": int(max(completion_times)),
    }


def select_action(state, weights, current_time):
    """
    Policy function: maps state -> action
    """
    def score(task):
        base = (
            weights["w_priority"] * task["priority"]
            - weights["w_duration"] * (task["duration"] ** 1.5)
            - 0.5 * current_time
        )

        urgency = task["priority"] / (task["duration"] + 1)

        noise = random.uniform(-2.0, 2.0)

        return base + (2 * urgency) + noise

    scores = [score(t) for t in state]

    # normalize for softmax stability
    max_score = max(scores)
    scores = [s - max_score for s in scores]

    TEMPERATURE = 5.0
    exp_scores = [math.exp(s / TEMPERATURE) for s in scores]
    total = sum(exp_scores)
    probs = [e / total for e in exp_scores]

    # sample
    r = random.random()
    cumulative = 0
    chosen_index = 0

    for i, p in enumerate(probs):
        cumulative += p
        if r <= cumulative:
            chosen_index = i
            break

    return chosen_index


def run_rl(tasks):
    if not tasks:
        return {
            "schedule": [],
            "metrics": {
                "avg_wait_time": 0,
                "throughput": 0,
                "tail_latency": 0,
            },
        }

    # ✅ merge weights correctly
    weights = {**DEFAULT_WEIGHTS, **load_learned_weights()}

    tasks = _normalize_tasks(tasks)
    schedule = []
    current_time = 0

    while tasks:
        chosen_index = select_action(tasks, weights, current_time)

        next_task = tasks.pop(chosen_index)

        start = current_time
        end = current_time + next_task["duration"]

        schedule.append(
            {
                "task_id": int(next_task["id"]),
                "start": int(start),
                "end": int(end),
                "score": 0.0,
            }
        )

        current_time = end

    return {
        "schedule": schedule,
        "metrics": _compute_metrics(schedule),
    }

def run_baseline(tasks):
    remaining_tasks = _normalize_tasks(tasks or [])
    schedule = []
    current_time = 0

    while remaining_tasks:
        next_task = max(
            remaining_tasks,
            key=lambda task: task["priority"] - 0.5 * task["duration"],
        )
        remaining_tasks.remove(next_task)

        start = current_time
        end = current_time + next_task["duration"]
        schedule.append(
            {
                "task_id": int(next_task["id"]),
                "start": int(start),
                "end": int(end),
                "score": 0.0,
            }
        )
        current_time = end

    return {
        "schedule": schedule,
        "metrics": _compute_metrics(schedule),
    }
