import os
import math
import random
import numpy as np
from pathlib import Path

import torch
import torch.nn as nn

from backend.scheduler.env import MAX_TASKS

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)

# Load model globally to ensure <100ms inference
state_size = 1 + (MAX_TASKS * 2)
action_size = MAX_TASKS
model = DQN(state_size, action_size)

model_path = Path(__file__).resolve().parent / "rl_model.pth"
MODEL_LOADED = False
try:
    if model_path.exists():
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()
        MODEL_LOADED = True
    else:
        print("WARNING: rl_model.pth not found, falling back to heuristic.")
except Exception as e:
    print(f"WARNING: failed to load RL model: {e}")

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

def get_state(tasks, current_time):
    state = [float(current_time)]
    for i in range(MAX_TASKS):
        if i < len(tasks):
            state.append(float(tasks[i].get("priority", 0)))
            state.append(float(tasks[i].get("duration", 0)))
        else:
            state.append(0.0)
            state.append(0.0)
    return np.array(state, dtype=np.float32)

def run_rl(tasks):
    if not tasks:
        return {
            "schedule": [],
            "metrics": _compute_metrics([])
        }

    tasks = _normalize_tasks(tasks)
    schedule = []
    current_time = 0

    while tasks:
        if MODEL_LOADED:
            state = get_state(tasks, current_time)
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            
            with torch.no_grad():
                q_values = model(state_tensor)
                
            # Mask invalid actions
            valid_actions = list(range(len(tasks)))
            masked_q_values = q_values.clone()
            mask = torch.ones_like(masked_q_values, dtype=torch.bool)
            mask[0, valid_actions] = False
            masked_q_values[mask] = -float('inf')
            
            chosen_index = torch.argmax(masked_q_values[0]).item()
        else:
            # Fallback heuristic
            def score(task):
                return task["priority"] - 0.5 * task["duration"]
            
            scores = [score(t) for t in tasks]
            chosen_index = scores.index(max(scores))

        next_task = tasks.pop(chosen_index)
        
        start = current_time
        end = current_time + next_task["duration"]
        
        schedule.append({
            "task_id": int(next_task["id"]),
            "start": int(start),
            "end": int(end),
            "score": 0.0
        })
        
        current_time = end

    return {
        "schedule": schedule,
        "metrics": _compute_metrics(schedule)
    }
