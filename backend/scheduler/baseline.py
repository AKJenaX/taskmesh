def baseline_schedule(tasks):
    current_time = 0
    schedule = []

    # Sort by priority (highest first)
    tasks_sorted = sorted(tasks, key=lambda x: x["priority"], reverse=True)

    for task in tasks_sorted:
        duration = task.get("duration", 1)

        start = current_time
        end = start + duration

        schedule.append({
            "task_id": task["id"],
            "start": start,
            "end": end,
            "score": 0.0
        })

        current_time = end

    return schedule


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
    for idx, task in enumerate(tasks or []):
        task_id = _to_int(_get(task, "id", idx + 1), idx + 1)
        duration = max(0, _to_int(_get(task, "duration", 0), 0))
        priority = _to_int(_get(task, "priority", 0), 0)
        normalized.append(
            {
                "id": task_id,
                "duration": duration,
                "priority": priority,
            }
        )
    return normalized


def _compute_metrics(schedule, final_time):
    if not schedule:
        return {
            "avg_wait_time": 0,
            "throughput": 0,
            "tail_latency": 0,
        }

    wait_times = [item["start"] for item in schedule]
    return {
        "avg_wait_time": int(sum(wait_times) / len(wait_times)),
        "throughput": int(len(schedule)),
        "tail_latency": int(final_time),
    }


def run_baseline(tasks):
    remaining_tasks = _normalize_tasks(tasks)
    current_time = 0
    schedule = []

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
        "metrics": _compute_metrics(schedule, current_time),
    }
