from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    title: str
    priority: int = Field(default=1, ge=1, le=5)
    duration_minutes: int = Field(default=30, ge=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ScheduleRequest(BaseModel):
    tasks: List[Task]


class ScheduleResponse(BaseModel):
    ordered_tasks: List[Task]
    score: float
    strategy: str = "baseline_priority"
