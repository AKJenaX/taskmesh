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
            "core": 0
        })

        current_time = end

    return schedule