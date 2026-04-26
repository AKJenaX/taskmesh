---
title: TaskMesh
emoji: 💻
colorFrom: green
colorTo: gray
sdk: docker
pinned: false
---

# 🚀 TaskMesh

> A reinforcement learning-based task scheduling system that reduces average wait time by **18%** by dynamically adapting scheduling decisions using a language-model policy.

## Live Demo

🔗 **Live API & Dashboard:** https://akj123-taskmesh.hf.space/docs

---

## Problem Statement

Task scheduling in operating systems, cloud clusters, and complex systems is inherently challenging due to dynamic workloads.

Traditional schedulers rely on static heuristics such as FIFO or fixed priority queues. These approaches fail to adapt to changing queue conditions. For example, executing a high-priority but long-running task too early can create severe bottlenecks, significantly increasing wait times for all subsequent tasks.

---

## Solution Overview

TaskMesh models scheduling as a Reinforcement Learning problem.

It uses a causal language model (**distilgpt2**) trained with Proximal Policy Optimization (PPO) via Hugging Face TRL.

- Environment state → converted into a text prompt  
- Model → generates an action (task index)  
- Action → selects the next task to schedule  

This allows the system to dynamically choose actions that optimize overall system efficiency instead of relying on fixed rules.

---

## Environment Design

TaskMesh implements a custom step-based RL environment (`TaskMeshEnv`) aligned with OpenEnv principles.

- **Task Generation:** Randomized tasks with varying durations (1–10) and priorities (1–10)  
- **State Representation:**  
  - Remaining tasks  
  - Current system time  
  - Schedule history  
  - Accumulated wait time  
- **Action Space:** Dynamic discrete indices mapping to tasks in the queue  

### Key Complexities

- **Dynamic Action Space:** Shrinks as tasks are completed  
- **Cascading Effects:** Early decisions significantly impact future latency  
- **Multi-Objective Trade-offs:** Balance priority, duration, and system-wide wait time  

---

## Why Reinforcement Learning

The scheduling problem is **state-dependent**, not rule-based.

Optimal decisions vary depending on queue composition:
- A long task should be delayed in a congested queue  
- The same task may be optimal when the queue is nearly empty  

Static heuristics assume fixed relationships and cannot adapt to such context.

Reinforcement Learning enables:
- Adaptive decision-making  
- Learning from environment feedback  
- Balancing short-term and long-term trade-offs  

---

## Reward Design

The reward function aligns local scheduling decisions with global system efficiency.

### Positive Signals
- Rewards selection of high-priority tasks (`+2.0 * priority`)

### Penalties
- Wait time penalty (`-1.0 * wait_time`)
- Duration penalty (`-0.5 * duration`)
- Repetitive scheduling penalty (`-1`)
- Episode-level penalties:
  - Total wait time  
  - Total completion time  

### Structure
- **Dense:** Immediate feedback at each step  
- **Sparse:** Final evaluation of full schedule  

---

## Results

Empirical benchmarking shows that the RL policy improves scheduling efficiency without degrading system stability.

| Metric | Baseline | TaskMesh (RL) | Improvement |
|--------|---------|--------------|-------------|
| **Average Wait Time** | 9.856 | 8.076 | ↓ **18.06%** |
| **Throughput** | 5.0 | 5.0 | Unchanged |
| **Tail Latency** | 28.38 | 28.38 | Unchanged |

---

## Training Insights

- **Episodes:** 200  
- **Training Signal:** Noisy and fluctuating  

### Why Noise Exists
- Stochastic task generation (different queues each episode)  
- Exploration during training  

Despite this, the final trained policy consistently achieves **~18% improvement in average wait time**, demonstrating effective learning.

![Reward Curve](scripts/reward_curve.png)

---

## Baseline Comparison

TaskMesh is evaluated against a static heuristic scheduler.

- **Strategy:** Priority-based greedy scheduling  
- **Logic:**  
  - Sort by priority  
  - Or use fixed scoring: `priority - 0.5 * duration`  

### Limitations
- Non-adaptive  
- Ignores deadlines  
- Greedy (no long-term optimization)  

RL overcomes these by learning context-aware scheduling strategies.

---

## Real-World Relevance

This environment reflects real-world scheduling scenarios such as:
- CPU task scheduling  
- Cloud job scheduling  
- Distributed system workloads  

The system models realistic trade-offs between latency, priority, and resource utilization.

---

## Architecture

- **Environment:** Custom `OpenEnvTaskMesh` simulator  
- **Policy Training:** PPO via `trl.PPOTrainer`  
- **Model:** distilgpt2 (text-based decision policy)  
- **Backend:** FastAPI  
- **Deployment:** Docker + Hugging Face Spaces  

---

## Training Setup

- **Model:** distilgpt2  
- **Framework:** Hugging Face TRL  
- **Episodes:** 200  

---

## Links

- **Live Demo:** https://akj123-taskmesh.hf.space/docs  
- **Blog / Explanation:** (coming soon)  
- **Video Walkthrough:** (coming soon)