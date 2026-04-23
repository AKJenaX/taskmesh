from typing import List

from backend.schemas import Task


def sort_tasks_by_priority(tasks: List[Task]) -> List[Task]:
    return sorted(
        tasks,
        key=lambda task: (-task.priority, task.duration_minutes, task.title.lower()),
    )
