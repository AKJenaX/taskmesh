# 🚀 TaskMesh — RL-Based Task Scheduling

TaskMesh is a lightweight **RL-inspired scheduling environment** that improves task ordering using reward-driven learning.

---

## 🧠 Problem

Traditional schedulers use fixed rules and cannot adapt, leading to higher wait time and latency.

👉 TaskMesh introduces a learning-based approach to optimize scheduling decisions.

---

## ⚙️ Approach

* Baseline: Priority-based scheduling
* RL Scheduler: Learns task ordering using weighted scoring (priority, deadline, duration)
* Training: Optimizes weights using reward feedback

---

## 📊 Results

| Metric       | Baseline | RL Scheduler | Improvement |
| ------------ | -------- | ------------ | ----------- |
| Avg Wait     | 5.60     | 5.00         | -10.7%      |
| Tail Latency | 13.00    | 10.00        | -23.1%      |

👉 RL consistently outperforms baseline.

---

## 📈 Training

* Episodes: 200
* Reward improved: **-67 → -9.6**
* Learned weights used for scheduling

---

## 🚀 Run

```bash
pip install -r requirements.txt
uvicorn backend.app:app --reload
python -m scripts.benchmark
```

---

## 🔌 API

POST `/schedule`

```json
{
  "tasks": [
    {
      "id": "task-1",
      "priority": 5,
      "duration_minutes": 30
    }
  ]
}
```

---

## 🎯 Hackathon Alignment

* RL environment (state → action → reward)
* Training loop with improvement
* Measurable performance gains

---

## 👥 Team

* Member A — Backend
* Member B — AI Scheduler
* Member C — Frontend

---

**Built for clarity, performance, and fast evaluation 🚀**
