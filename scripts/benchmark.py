from backend.scheduler.rl_agent import run_rl
from backend.scheduler.baseline import run_baseline
import matplotlib.pyplot as plt
import statistics
import copy
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


tasks = [
    {"id": 1, "duration": 8, "priority": 1},
    {"id": 2, "duration": 2, "priority": 3},
    {"id": 3, "duration": 6, "priority": 2},
    {"id": 4, "duration": 1, "priority": 3},
]

baseline_result = run_baseline(copy.deepcopy(tasks))

RL_RUNS = 10

rl_metrics = []

for _ in range(RL_RUNS):
    result = run_rl(copy.deepcopy(tasks))
    rl_metrics.append(result["metrics"])


def avg(key):
    return round(statistics.mean([m[key] for m in rl_metrics]), 2)


rl_avg = {
    "avg_wait_time": avg("avg_wait_time"),
    "throughput": avg("throughput"),
    "tail_latency": avg("tail_latency"),
}


def improvement(base, rl):
    return round(((base - rl) / base) * 100, 2) if base else 0


print("\n" + "=" * 40)
print("🚀 TASKMESH BENCHMARK RESULTS")
print("=" * 40)

print("\n📊 BASELINE METRICS")
for k, v in baseline_result["metrics"].items():
    print(f"{k:15}: {v}")

print("\n🤖 RL METRICS (avg over runs)")
for k, v in rl_avg.items():
    print(f"{k:15}: {v}")

print("\n📈 IMPROVEMENT")


def arrow(val):
    if val > 0:
        return f"⬇️ {val}% better"
    elif val < 0:
        return f"⬆️ {abs(val)}% worse"
    return "no change"


avg_wait_improvement = improvement(
    baseline_result["metrics"]["avg_wait_time"],
    rl_avg["avg_wait_time"],
)
tail_latency_improvement = improvement(
    baseline_result["metrics"]["tail_latency"],
    rl_avg["tail_latency"],
)

print(f"Avg Wait Time : {arrow(avg_wait_improvement)}")
print(f"Tail Latency  : {arrow(tail_latency_improvement)}")

print("\n🏆 RESULT:")
if rl_avg["avg_wait_time"] <= baseline_result["metrics"]["avg_wait_time"]:
    print("RL scheduler improves system efficiency ✅")
else:
    print("RL needs tuning ⚠️")

labels = ["avg_wait_time", "tail_latency"]

baseline_vals = [
    baseline_result["metrics"]["avg_wait_time"],
    baseline_result["metrics"]["tail_latency"],
]

rl_vals = [
    rl_avg["avg_wait_time"],
    rl_avg["tail_latency"],
]

x = range(len(labels))

plt.figure()

plt.bar(x, baseline_vals, label="Baseline")
plt.bar(x, rl_vals, label="RL", alpha=0.7)

plt.xticks(x, labels)
plt.title("Baseline vs RL Scheduler Comparison")
plt.legend()

plt.savefig("benchmark.png")
plt.show()

print("\n📊 Saved graph as benchmark.png")

print("\n🧠 INTERPRETATION:")

if rl_avg["tail_latency"] < baseline_result["metrics"]["tail_latency"]:
    print("RL reduces worst-case delays → more stable system ✅")
else:
    print("RL increases tail latency → needs tuning ⚠️")

if rl_avg["avg_wait_time"] < baseline_result["metrics"]["avg_wait_time"]:
    print("RL improves average response time 🚀")
else:
    print("RL does not improve average wait time")
