def compute_metrics(schedule):
    if not schedule:
        return {
            "avg_wait_time": 0,
            "throughput": 0,
            "tail_latency": 0
        }

    wait_times = [task["start"] for task in schedule]

    avg_wait_time = sum(wait_times) / len(wait_times)
    throughput = len(schedule)
    tail_latency = max(wait_times)

    return {
        "avg_wait_time": avg_wait_time,
        "throughput": throughput,
        "tail_latency": tail_latency
    }