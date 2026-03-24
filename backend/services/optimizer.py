from collections import defaultdict
from schemas import CourseOut, OptimizationSuggestion

LATE_EVENING_THRESHOLD = 19 * 60
LARGE_GAP_MINUTES      = 90
HEAVY_DAY_CLASSES      = 4


def _to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _day_label(d: str) -> str:
    return {
        "M": "Monday",   "T": "Tuesday",  "W": "Wednesday",
        "R": "Thursday", "F": "Friday",   "S": "Saturday", "U": "Sunday",
    }.get(d, d)


def analyze_schedule(courses: list[CourseOut]) -> tuple[list[OptimizationSuggestion], int]:
    suggestions: list[OptimizationSuggestion] = []
    penalty = 0

    for c in courses:
        if _to_minutes(c.start_time) >= LATE_EVENING_THRESHOLD:
            suggestions.append(OptimizationSuggestion(
                category="late_evening",
                message=f"'{c.name}' starts at {c.start_time}, which is after 7 PM. Evening classes can impact sleep and study time.",
                severity="warning",
            ))
            penalty += 10

    day_slots: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
    for c in courses:
        for day in c.days:
            day_slots[day].append((_to_minutes(c.start_time), _to_minutes(c.end_time), c.name))

    for day, slots in day_slots.items():
        slots.sort()
        for k in range(len(slots) - 1):
            gap = slots[k + 1][0] - slots[k][1]
            if gap > LARGE_GAP_MINUTES:
                suggestions.append(OptimizationSuggestion(
                    category="gap",
                    message=f"There is a {gap}-minute gap between '{slots[k][2]}' and '{slots[k+1][2]}' on {_day_label(day)}.",
                    severity="info",
                ))
                penalty += 5

    day_count: dict[str, int] = defaultdict(int)
    for c in courses:
        for day in c.days:
            day_count[day] += 1

    for d, cnt in day_count.items():
        if cnt >= HEAVY_DAY_CLASSES:
            suggestions.append(OptimizationSuggestion(
                category="workload",
                message=f"{_day_label(d)} has {cnt} classes. Consider redistributing to avoid burnout.",
                severity="warning",
            ))
            penalty += 8

    if len(day_count) > 1:
        counts = list(day_count.values())
        if max(counts) - min(counts) >= 3:
            suggestions.append(OptimizationSuggestion(
                category="workload",
                message=f"Workload is unevenly distributed (range: {min(counts)}–{max(counts)} classes/day).",
                severity="info",
            ))
            penalty += 5

    return suggestions, max(0, 100 - penalty)
