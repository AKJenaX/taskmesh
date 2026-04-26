import os
import sys
import numpy as np

try:
    from openenv import Environment
except ImportError:
    class Environment:
        pass

from backend.scheduler.env import TaskEnv, MAX_TASKS

class TaskMeshOpenEnv(Environment):
    """
    OpenEnv compliant wrapper for the TaskMesh task scheduling environment.
    Conforms to the standard Gym API (reset, step).
    """
    def __init__(self, tasks=None):
        super().__init__()
        
        # Provide fallback generic tasks if initialized raw
        if tasks is None:
            tasks = [
                {"id": 1, "priority": 5, "duration": 15},
                {"id": 2, "priority": 1, "duration": 45},
                {"id": 3, "priority": 3, "duration": 30}
            ]
            
        self.internal_env = TaskEnv(tasks)
        
        self.action_space = MAX_TASKS
        self.observation_space = 1 + (MAX_TASKS * 2)

    def reset(self, seed=None):
        state = self.internal_env.reset()
        return state, {}

    def step(self, action):
        state, reward, done = self.internal_env.step(action)
        
        terminated = done
        truncated = False
        info = {
            "scheduled": self.internal_env.scheduled,
            "wait_time": self.internal_env.time
        }
        
        return state, float(reward), terminated, truncated, info

    def get_valid_actions(self):
        return self.internal_env.get_valid_actions()
