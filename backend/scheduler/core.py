from typing import Dict

from backend.schemas import ScheduleRequest
from backend.scheduler.baseline import sort_tasks_by_priority


def run_scheduler(request: ScheduleRequest) -> Dict:
    ordered_tasks = sort_tasks_by_priority(request.tasks)

    if not ordered_tasks:
        return {
            "ordered_tasks": [],
            "score": 0.0,
            "strategy": "baseline_priority",
        }

    total_priority = sum(task.priority for task in ordered_tasks)
    score = round(total_priority / len(ordered_tasks), 2)

    return {
        "ordered_tasks": ordered_tasks,
        "score": score,
        "strategy": "baseline_priority",
    }
