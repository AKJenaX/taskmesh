import random


class TaskMeshEnv:
    def __init__(self):
        self.rng = random.Random(7)
        self.tasks = []
        self.current_time = 0
        self.done = False
        self.schedule = []
        self.total_wait_time = 0
        self.total_completion_time = 0
        self.last_priorities = []

    def reset(self):
        self.tasks = []

        for i in range(5):
            self.tasks.append({
                "id": i,
                "duration": self.rng.randint(1, 10),
                "priority": self.rng.randint(1, 10),
            })

        self.current_time = 0
        self.done = False
        self.schedule = []
        self.total_wait_time = 0
        self.total_completion_time = 0
        self.last_priorities = []

        return list(self.tasks)

    def step(self, action):
        try:
            if self.done:
                return list(self.tasks), -10, self.done, {}

            if not isinstance(action, int) or action < 0 or action >= len(self.tasks):
                return list(self.tasks), -10, self.done, {}

            task = self.tasks.pop(action)
            start = self.current_time
            wait_time = start
            priority = task["priority"]
            duration = task["duration"]
            end = start + duration

            self.schedule.append(
                {
                    "task_id": task["id"],
                    "start": start,
                    "end": end,
                }
            )
            self.current_time = end
            self.total_wait_time += wait_time
            self.total_completion_time = self.current_time
            self.done = len(self.tasks) == 0

            reward = -1.0 * wait_time - 0.5 * duration + 2.0 * priority

            self.last_priorities.append(priority)
            if (
                len(self.last_priorities) >= 2
                and self.last_priorities[-1] == self.last_priorities[-2]
            ):
                reward -= 1

            if self.done:
                final_bonus = (
                    -0.2 * self.total_wait_time
                    -0.1 * self.total_completion_time
                )
                reward += final_bonus

            return list(self.tasks), reward, self.done, {}
        except Exception:
            return list(self.tasks), -10, self.done, {}

    def state(self):
        return {
            "remaining_tasks": list(self.tasks),
            "current_time": self.current_time,
            "schedule": list(self.schedule),
            "total_wait_time": self.total_wait_time,
        }
