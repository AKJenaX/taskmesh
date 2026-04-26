import numpy as np

MAX_TASKS = 20

class TaskEnv:
    def __init__(self, tasks):
        self.original_tasks = [dict(t) for t in tasks]
        self.max_tasks = MAX_TASKS
        self.reset()

    def reset(self):
        self.tasks = [dict(t) for t in self.original_tasks]
        self.time = 0
        self.done = False
        self.scheduled = []
        return self._get_state()

    def _get_state(self):
        # State: [current_time] + [task1_prio, task1_dur, ...] + [0, 0] padding
        state = [float(self.time)]
        
        for i in range(self.max_tasks):
            if i < len(self.tasks):
                state.append(float(self.tasks[i].get("priority", 0)))
                state.append(float(self.tasks[i].get("duration", 0)))
            else:
                state.append(0.0)
                state.append(0.0)
                
        return np.array(state, dtype=np.float32)

    def get_valid_actions(self):
        return list(range(len(self.tasks)))

    def step(self, action):
        if self.done:
            return self._get_state(), 0.0, True

        valid_actions = self.get_valid_actions()
        if action not in valid_actions:
            return self._get_state(), -100.0, self.done

        task = self.tasks.pop(action)
        
        wait_time = self.time
        
        # Simple stable reward: negative wait_time + bonus for scheduling high priority early
        reward = (task.get("priority", 1) * 10.0) - wait_time
        
        start = self.time
        end = start + task.get("duration", 1)
        
        self.scheduled.append({
            "task_id": task.get("id", 0),
            "start": int(start),
            "end": int(end),
            "score": 0.0
        })
        
        self.time = end
        self.done = len(self.tasks) == 0
        
        return self._get_state(), float(reward), self.done
