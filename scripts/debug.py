from backend.scheduler.core import run_scheduler, score_task, LEARNED_WEIGHTS
from backend.scheduler.baseline import baseline_schedule

# New test data where priority and deadline conflict
request = {
    "tasks": [
        {"id": "1", "title": "Task A", "priority": 5, "deadline": 15, "duration": 2},
        {"id": "2", "title": "Task B", "priority": 3, "deadline": 5, "duration": 3},
        {"id": "3", "title": "Task C", "priority": 4, "deadline": 20, "duration": 1},
        {"id": "4", "title": "Task D", "priority": 2, "deadline": 8, "duration": 4},
        {"id": "5", "title": "Task E", "priority": 1, "deadline": 3, "duration": 5},
    ],
    "constraints": {}
}

print("RL Scores:")
for t in request["tasks"]:
    score = score_task(t, LEARNED_WEIGHTS)
    print(f"  Task {t['id']}: priority={t['priority']}, deadline={t['deadline']}, duration={t['duration']} -> score={score:.2f}")

print("\nBASELINE order (priority only):")
b = baseline_schedule(request["tasks"])
for t in b:
    print(f"  Task {t['task_id']}")

print("\nRL order (deadline-first):")
r = run_scheduler(request, algorithm="rl")
for t in r["schedule"]:
    print(f"  Task {t['task_id']}")