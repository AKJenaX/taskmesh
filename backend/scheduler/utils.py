from typing import Iterable


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


def average(values: Iterable[int]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)
