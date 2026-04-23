from fastapi import APIRouter

from backend.schemas import ScheduleRequest, ScheduleResponse
from backend.scheduler.core import run_scheduler


router = APIRouter()


@router.post("/schedule", response_model=ScheduleResponse)
def schedule_tasks(payload: ScheduleRequest) -> ScheduleResponse:
    result = run_scheduler(payload)
    return ScheduleResponse(**result)
