import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.scheduler.openenv_env import TaskMeshOpenEnv

env = TaskMeshOpenEnv()

class PolicyNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, action_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.softmax(self.fc2(x))

state_size = env.observation_space
action_size = env.action_space
policy = PolicyNetwork(state_size, action_size)
optimizer = optim.Adam(policy.parameters(), lr=0.01)

episodes = 300
rewards_history = []
gamma = 0.99

print("Training Lightweight RL Agent via Policy Gradients...")
for ep in range(episodes):
    state, _ = env.reset()
    state = torch.FloatTensor(state).unsqueeze(0)
    
    log_probs = []
    rewards = []
    
    done = False
    while not done:
        valid_actions = env.get_valid_actions()
        probs = policy(state)
        
        # Mask invalid actions
        mask = torch.zeros_like(probs)
        mask[0, valid_actions] = 1.0
        masked_probs = probs * mask
        if masked_probs.sum() == 0:
            masked_probs = mask / mask.sum()
        else:
            masked_probs /= masked_probs.sum()
            
        dist = torch.distributions.Categorical(masked_probs)
        action = dist.sample()
        
        next_state, reward, terminated, truncated, _ = env.step(action.item())
        
        log_probs.append(dist.log_prob(action))
        rewards.append(reward)
        
        state = torch.FloatTensor(next_state).unsqueeze(0)
        done = terminated or truncated
        
    # Discounted rewards
    discounted_rewards = []
    R = 0
    for r in reversed(rewards):
        R = r + gamma * R
        discounted_rewards.insert(0, R)
    discounted_rewards = torch.tensor(discounted_rewards)
    if len(discounted_rewards) > 1:
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-9)
        
    loss = []
    for log_prob, R in zip(log_probs, discounted_rewards):
        loss.append(-log_prob * R)
    
    if loss:
        loss = torch.cat(loss).sum()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    total_reward = sum(rewards)
    rewards_history.append(total_reward)

# Plot Reward Curve
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'assets'), exist_ok=True)
plt.figure(figsize=(10, 5))
plt.plot(rewards_history, label="Policy Gradient Reward", color='#00e5ff')
plt.title("OpenEnv Training Progress")
plt.xlabel("Episode")
plt.ylabel("Cumulative Reward")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(os.path.dirname(__file__), '..', 'assets', 'reward_curve.png'), bbox_inches='tight')
print("Saved reward_curve.png")
