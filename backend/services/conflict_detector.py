from schemas import CourseOut, ConflictDetail


def _days_set(days_str: str) -> set[str]:
    return set(days_str.upper())


def _to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def detect_conflicts(courses: list[CourseOut]) -> list[ConflictDetail]:
    conflicts: list[ConflictDetail] = []
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            a, b = courses[i], courses[j]
            shared_days = _days_set(a.days) & _days_set(b.days)
            if not shared_days:
                continue
            a_start = _to_minutes(a.start_time)
            a_end   = _to_minutes(a.end_time)
            b_start = _to_minutes(b.start_time)
            b_end   = _to_minutes(b.end_time)
            if a_start < b_end and b_start < a_end:
                conflicts.append(ConflictDetail(
                    course_a=a,
                    course_b=b,
                    overlap_days="".join(sorted(shared_days)),
                ))
    return conflicts
