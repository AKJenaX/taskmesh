import os
import sys
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.scheduler.env import TaskEnv, MAX_TASKS

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

def train():
    state_size = 1 + (MAX_TASKS * 2)
    action_size = MAX_TASKS
    
    model = DQN(state_size, action_size)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    episodes = 500
    gamma = 0.95
    epsilon = 1.0
    epsilon_min = 0.05
    epsilon_decay = 0.99
    
    print("Starting fast RL training...")
    
    for e in range(episodes):
        # Generate random task set
        num_tasks = random.randint(5, 10)
        tasks = []
        for i in range(num_tasks):
            tasks.append({
                "id": i + 1,
                "priority": random.randint(1, 5),
                "duration": random.randint(10, 60)
            })
            
        env = TaskEnv(tasks)
        state = env.reset()
        state = torch.FloatTensor(state).unsqueeze(0)
        
        total_reward = 0
        done = False
        
        while not done:
            valid_actions = env.get_valid_actions()
            
            if random.random() <= epsilon:
                action = random.choice(valid_actions)
            else:
                with torch.no_grad():
                    q_values = model(state)
                    
                    # Mask invalid actions
                    masked_q_values = q_values.clone()
                    mask = torch.ones_like(masked_q_values, dtype=torch.bool)
                    mask[0, valid_actions] = False
                    masked_q_values[mask] = -float('inf')
                    
                    action = torch.argmax(masked_q_values[0]).item()
            
            next_state, reward, done = env.step(action)
            next_state = torch.FloatTensor(next_state).unsqueeze(0)
            total_reward += reward
            
            # Simple online update (no replay buffer for extreme speed)
            q_values = model(state)
            next_q_values = model(next_state)
            
            target_q = q_values.clone()
            if done:
                target_q[0][action] = reward
            else:
                # Mask next actions
                next_valid = env.get_valid_actions()
                next_masked = next_q_values.clone()
                next_mask = torch.ones_like(next_masked, dtype=torch.bool)
                if next_valid:
                    next_mask[0, next_valid] = False
                next_masked[next_mask] = -float('inf')
                
                target_q[0][action] = reward + gamma * torch.max(next_masked[0]).item()
                
            loss = criterion(q_values, target_q)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            state = next_state
            
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay
            
        if (e + 1) % 50 == 0:
            print(f"Episode {e+1}/{episodes} | Total Reward: {total_reward:.2f} | Epsilon: {epsilon:.2f}")

    # Save model
    model_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'scheduler', 'rl_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f"Training complete! Model saved to {model_path}")

if __name__ == "__main__":
    train()
