from typing import List

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    duration: int = Field(gt=0)
    priority: int = Field(ge=0)


class RequestModel(BaseModel):
    tasks: List[Task] = Field(default_factory=list)
    algorithm: str


class ScheduleItem(BaseModel):
    task_id: int
    start: int
    end: int
    score: float


class Metrics(BaseModel):
    avg_wait_time: int
    throughput: int
    tail_latency: int


class ResponseModel(BaseModel):
    schedule: List[ScheduleItem]
    metrics: Metrics
