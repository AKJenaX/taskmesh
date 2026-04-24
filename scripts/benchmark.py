from backend.scheduler.core import run_scheduler


def make_request():
    return {
        "tasks": [
            {"id": "1", "title": "Task A", "priority": 2, "deadline": 10, "duration": 5},
            {"id": "2", "title": "Task B", "priority": 5, "deadline": 5, "duration": 3},
            {"id": "3", "title": "Task C", "priority": 1, "deadline": 15, "duration": 2},
            {"id": "4", "title": "Task D", "priority": 3, "deadline": 7, "duration": 4},
            {"id": "5", "title": "Task E", "priority": 4, "deadline": 6, "duration": 1},
        ],
        "constraints": {}
    }


def print_table(results):
    print("\nAlgorithm     | Avg Wait | Throughput | Tail Latency")
    print("-----------------------------------------------------")

    for algo, metrics in results.items():
        print(f"{algo:<13} | {metrics['avg_wait_time']:<8.2f} | {metrics['throughput']:<10} | {metrics['tail_latency']:<12.2f}")


def main():
    request = make_request()

    results = {}

    for algo in ["baseline", "rl"]:
        output = run_scheduler(request, algorithm=algo)
        metrics = output["metrics"]
        results[algo] = metrics

    print_table(results)


if __name__ == "__main__":
    main()