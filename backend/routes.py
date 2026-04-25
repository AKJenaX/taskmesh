from fastapi import APIRouter

from backend.schemas import Metrics, RequestModel, ResponseModel, ScheduleItem

try:
    from backend.scheduler.adaptive_scheduler import run_rl
except Exception:
    run_rl = None

try:
    from backend.scheduler.baseline import run_baseline
except Exception:
    run_baseline = None


router = APIRouter()


def run_baseline_stub(tasks):
    if not tasks:
        return {
            "schedule": [],
            "metrics": {
                "avg_wait_time": 0,
                "throughput": 0,
                "tail_latency": 0,
            },
        }

    first_task = tasks[0]
    return {
        "schedule": [
            {
                "task_id": first_task.id,
                "start": 0,
                "end": first_task.duration,
                "core": 0,
            }
        ],
        "metrics": {
            "avg_wait_time": 0,
            "throughput": 1,
            "tail_latency": 0,
        },
    }


def run_rl_stub(tasks):
    return run_baseline_stub(tasks)


def validate_and_normalize(result):
    if not isinstance(result, dict):
        return None

    if "schedule" not in result or "metrics" not in result:
        return None

    schedule = result["schedule"]
    metrics = result["metrics"]

    if not isinstance(schedule, list):
        return None

    validated_schedule = []
    for item in schedule:
        if not isinstance(item, dict):
            return None

        required_schedule_fields = ("task_id", "start", "end", "core")
        if any(field not in item for field in required_schedule_fields):
            return None

        task_id = item["task_id"]
        start = item["start"]
        end = item["end"]
        core = item["core"]

        if not all(isinstance(value, int) for value in (task_id, start, end, core)):
            return None

        validated_schedule.append(
            {
                "task_id": task_id,
                "start": start,
                "end": end,
                "core": core,
            }
        )

    if not isinstance(metrics, dict):
        return None

    required_metric_fields = ("avg_wait_time", "throughput", "tail_latency")
    if any(field not in metrics for field in required_metric_fields):
        return None

    avg_wait_time = metrics["avg_wait_time"]
    throughput = metrics["throughput"]
    tail_latency = metrics["tail_latency"]

    if not all(
        isinstance(value, (int, float))
        for value in (avg_wait_time, throughput, tail_latency)
    ):
        return None

    validated_metrics = {
        "avg_wait_time": avg_wait_time,
        "throughput": throughput,
        "tail_latency": tail_latency,
    }

    return {
        "schedule": validated_schedule,
        "metrics": validated_metrics,
    }


def get_scheduler_func(algo):
    if algo == "baseline":
        return run_baseline if run_baseline else run_baseline_stub
    if algo == "rl":
        return run_rl if run_rl else run_rl_stub
    return None


@router.post("/simulate", response_model=ResponseModel)
def simulate(payload: RequestModel) -> ResponseModel:
    fallback = ResponseModel(
        schedule=[],
        metrics=Metrics(
            avg_wait_time=0,
            throughput=0,
            tail_latency=0,
        ),
    )

    try:
        algo = (payload.algorithm or "").strip().lower()
        tasks = payload.tasks or []

        if algo == "baseline":
            func = run_baseline if run_baseline else run_baseline_stub

        elif algo == "rl":
            func = run_rl if run_rl else run_rl_stub

        else:
            return fallback

        print(f"[DEBUG] Using function: {func.__name__}")
        result = func(tasks)

        validated = validate_and_normalize(result)
        if validated is None:
            return fallback

        normalized_metrics = {
            "avg_wait_time": int(validated["metrics"]["avg_wait_time"]),
            "throughput": int(validated["metrics"]["throughput"]),
            "tail_latency": int(validated["metrics"]["tail_latency"]),
        }

        return ResponseModel(
            schedule=[ScheduleItem(**item) for item in validated["schedule"]],
            metrics=Metrics(**normalized_metrics),
        )
    except Exception:
        return fallback


@router.post("/schedule")
def schedule(payload: RequestModel):
    fallback = {
        "ordered_tasks": [],
        "score": 0,
        "strategy": "error",
    }

    try:
        algo = (payload.algorithm or "").strip().lower()
        func = get_scheduler_func(algo)
        if func is None:
            return fallback

        result = func(payload.tasks)

        validated = validate_and_normalize(result)
        if validated is None:
            return fallback

        ordered_tasks = [item["task_id"] for item in validated["schedule"]]
        score = int(validated["metrics"]["throughput"])

        return {
            "ordered_tasks": ordered_tasks,
            "score": score,
            "strategy": payload.algorithm,
        }
    except Exception:
        return fallback
