---
title: TaskMesh
emoji: 💻
colorFrom: green
colorTo: gray
sdk: docker
pinned: false
---
# 🚀 TaskMesh - Adaptive Task Scheduling System
> Achieves ~18% reduction in average wait time using reward-driven adaptive scheduling.

🔗 **Live Demo:** https://akj123-taskmesh.hf.space/docs

---

## 🧠 Overview

TaskMesh is a learning-based adaptive scheduling system that optimizes task execution order using reward-driven policy updates.

Unlike traditional schedulers (FIFO, priority-only), TaskMesh dynamically balances:

- Task priority
- Execution duration
- System wait time

to minimize overall latency and improve efficiency.

---

## 🧠 Key Insight

Instead of using fixed scheduling rules, TaskMesh learns to balance multiple competing factors dynamically through reward feedback, enabling better real-time decision-making.

---

## ⚙️ Key Features

- 🔹 Policy-based task selection (state → action)
- 🔹 Reward-driven learning across episodes
- 🔹 Real-time scheduling via API
- 🔹 Benchmark comparison vs baseline
- 🔹 Fully deployed and interactive demo

---

## 📊 Results

| Metric | Baseline | TaskMesh |
|--------|--------|----------|
| Avg Wait Time | Higher | ↓ Improved (~18%) |
| Throughput | Same | Same |
| Adaptability | None | High |

---

## 🧪 Try It Yourself

Go to:
👉 https://akj123-taskmesh.hf.space/docs

Use:
- `/schedule` to generate optimized schedules
- `/simulate` to test scenarios

---

## 📈 Training Progress

![Reward Curve](./reward_plot.png)

---
## 🎬 Demo Walkthrough

1. Open the live API: https://akj123-taskmesh.hf.space/docs  
2. Use `/schedule` endpoint  
3. Input a list of tasks  
4. Observe optimized execution order  

TaskMesh dynamically prioritizes tasks based on reward-driven policy, reducing wait time and improving scheduling efficiency.

---

## 🧠 How It Works

1. Environment simulates task scheduling
2. Policy selects next task based on weighted scoring
3. Reward signals guide weight optimization
4. Best-performing weights are retained

---

## 🏁 Conclusion

TaskMesh demonstrates how reward-driven adaptive systems can outperform static scheduling strategies in dynamic environments.