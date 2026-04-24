class TaskEnv:
    def __init__(self, tasks):
        self.original_tasks = [dict(t) for t in tasks]
        self.reset()

    def reset(self):
        self.tasks = [dict(t) for t in self.original_tasks]
        self.time = 0
        self.done = False
        self.scheduled = []
        self.steps = 0
        self.last_priority = None
        return self._get_state()

    def _get_state(self):
        return [dict(t) for t in self.tasks]

    def step(self, action):
        if self.done:
            return self._get_state(), 0.0, True

        self.steps += 1
        reward = 0.0

        if not (0 <= action < len(self.tasks)):
            reward = -5.0
            done = self.steps >= 500
            return self._get_state(), reward, done

        task = self.tasks.pop(action)
        wait_time = max(0, self.time)
        reward += task["priority"]
        reward -= wait_time * 0.1

        if self.last_priority is not None and task["priority"] >= self.last_priority:
            reward += 2.0
        self.last_priority = task["priority"]

        start = self.time
        end = start + task["duration"]
        self.scheduled.append({
            "task_id": task["id"],
            "start": start,
            "end": end,
            "core": 0
        })
        self.time = end

        done = len(self.tasks) == 0 or self.steps >= 500
        self.done = done
        return self._get_state(), reward, done

